#!/usr/bin/env python3
"""
Obsidian Vault → 静态知识库站点生成器
用法: python3 generate.py [--vault VAULT_DIR] [--output OUTPUT_DIR] [--host HOST] [--port PORT]
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

import yaml
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension


# ─────────────────────────── 配置 ───────────────────────────

VAULT_DIR = Path("/home/ubuntu/Obsidian")
OUTPUT_DIR = Path("/home/ubuntu/Obsidian/site")
HOST = "0.0.0.0"
PORT = 5500

# area 别名（URL 友好）
AREA_ALIASES = {
    "亚马逊运营": "amazon",
    "投资-量化": "quant",
    "跨境独立站": "website",
    "社交媒体": "social",
    "学习-一建": "exam",
    "AI助手对话记录": "ai",
}

# area 中文名
AREA_LABELS = {
    "亚马逊运营": "亚马逊运营",
    "投资-量化": "投资 · 量化",
    "跨境独立站": "跨境独立站",
    "社交媒体": "社交媒体",
    "学习-一建": "一建考证",
    "AI助手对话记录": "AI 助手",
}

# type 中文名
TYPE_LABELS = {
    "entity": "实体",
    "concept": "概念",
    "comparison": "对比",
    "query": "问答",
    "sop": "流程",
    "raw": "原始",
    "index": "索引",
    "log": "日志",
    "summary": "总结",
    "article": "文章",
}

# nav 顺序
AREA_ORDER = ["亚马逊运营", "投资-量化", "跨境独立站", "社交媒体", "学习-一建", "AI助手对话记录"]

# type → 子目录映射（与 generate_site 里的 TYPE_SUBDIR 保持一致）
TYPE_SUBDIR = {
    "entity": "entities",
    "concept": "concepts",
    "sop": "sop",
    "summary": "summaries",
    "article": "articles",
}


# ─────────────────────────── 解析 ───────────────────────────

FRONTMT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")

# heading levels to keep (don't collapse)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """手动解析 Obsidian frontmatter，不依赖 yaml 库"""
    m = FRONTMT_RE.match(content)
    if not m:
        return {}, content
    raw_fm = m.group(1)
    fm = {}

    for line in raw_fm.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ": " in line:
            key, val = line.split(": ", 1)
            key = key.strip()
            val = val.strip().strip("'\"")

            # 列表字段
            if val.startswith("["):
                # 尝试 JSON 解析（wikilink 数组已转成 JSON）
                try:
                    fm[key] = json.loads(val)
                    continue
                except Exception:
                    pass
                # 去掉 [ ]，按逗号分割
                inner = val.strip("[]")
                items = [s.strip().strip("'\"").strip("|") for s in inner.split(",")]
                fm[key] = [re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", s) for s in items if s]
            else:
                # 标量
                fm[key] = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", val)

    body = content[m.end():]
    return fm, body


def slugify(text: str) -> str:
    """abc-xyz"""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text


def render_markdown(text: str) -> str:
    """把 md 转成 HTML（不安全，仅内部用）"""
    md = markdown.Markdown(
        extensions=[
            FencedCodeExtension(),
            TableExtension(),
            TocExtension(permalink=True),
            CodeHiliteExtension(css_class="highlight"),
            "nl2br",
            "sane_lists",
        ]
    )
    # 处理 wikilink → <a>
    text = WIKILINK_RE.sub(r'<span class="wikilink">\1</span>', text)
    text = MD_LINK_RE.sub(r'<a href="\2">\1</a>', text)
    html = md.convert(text)
    # 清理空段落
    html = re.sub(r"<p>\s*</p>", "", html)
    return html


def extract_headings(text: str, n=3) -> list[tuple[str, str]]:
    """提取前 n 级标题，用于 TOC"""
    headings = []
    for line in text.split("\n"):
        m = HEADING_RE.match(line.strip())
        if m:
            level, title = len(m.group(1)), m.group(2).strip()
            if level <= n:
                anchor = slugify(title)
                headings.append((level, title, anchor))
    return headings


def read_all_pages(vault: Path) -> list[dict]:
    """扫描 vault，返回所有页面列表"""
    pages = []
    for md_file in vault.rglob("*.md"):
        rel = md_file.relative_to(vault)
        parts = rel.parts
        # 跳过非 area 目录下的文件（如 site_generator 本身）
        if len(parts) < 2 or parts[0] != "Areas":
            continue

        area = parts[1]
        sub_parts = parts[2:] if len(parts) > 2 else ()
        # sub_parts 最后一段可能是 index.md / SCHEMA.md 等，需要去掉 .md 后缀
        sub_parts = tuple(
            s[:-3] if s.endswith(".md") else s for s in sub_parts
        )
        sub_path = "/".join(sub_parts) + "/" if sub_parts else ""
        basename = md_file.stem  # 已经不含 .md 了（stem 就是去掉扩展名的部分）

        content = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)

        page_type = fm.get("type", "")
        if not page_type:
            # 从路径推断
            if any("concepts" in s for s in parts):
                page_type = "concept"
            elif any("entities" in s for s in parts):
                page_type = "entity"
            elif any("raw" in s for s in parts):
                page_type = "raw"
            elif any("SOP" in s.upper() or "sop" in s for s in parts):
                page_type = "sop"
            elif any("summaries" in s for s in parts):
                page_type = "summary"

        title = fm.get("title", md_file.stem)
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        created = fm.get("created", "")
        updated = fm.get("updated", "")
        sources = fm.get("sources", [])
        related = fm.get("related", [])
        confidence = fm.get("confidence", "")
        description = ""
        for line in body.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("!["):
                description = line
                if len(description) > 120:
                    description = description[:120] + "…"
                break

        html_body = render_markdown(body)
        headings = extract_headings(body)

        # 按 type 决定输出子目录和 URL
        area_slug = AREA_ALIASES.get(area, area)
        type_subdir = TYPE_SUBDIR.get(page_type)
        if type_subdir:
            page_url = f"{area_slug}/{type_subdir}/{basename}.html"
        else:
            page_url = f"{area_slug}/{basename}.html"

        pages.append({
            "path": str(rel),
            "area": area,
            "area_label": AREA_LABELS.get(area, area),
            "area_slug": area_slug,
            "type_subdir": type_subdir or "",
            "sub_path": sub_path,
            "filename": md_file.name,
            "basename": basename,
            "type": page_type,
            "type_label": TYPE_LABELS.get(page_type, page_type),
            "url": page_url,
            "title": title,
            "tags": tags,
            "created": created,
            "updated": updated,
            "sources": sources,
            "related": related,
            "confidence": confidence,
            "description": description,
            "html_body": html_body,
            "headings": headings,
        })
    return pages


# ─────────────────────────── 模板数据 ───────────────────────────

def build_site_data(pages: list[dict]) -> dict:
    """构建传递给模板的全部数据"""
    # 按 area 分组
    by_area = defaultdict(list)
    for p in pages:
        by_area[p["area"]].append(p)

    # 统计
    stats = {area: len(pgs) for area, pgs in by_area.items()}

    # 全部标签
    all_tags = set()
    for p in pages:
        for t in p.get("tags", []):
            all_tags.add(t)
    all_tags = sorted(all_tags)

    # 最新页面（按 updated 或 created）
    def sort_key(p):
        return p.get("updated") or p.get("created") or ""
    recent = sorted(pages, key=sort_key, reverse=True)[:10]

    return {
        "pages": pages,
        "by_area": dict(by_area),
        "stats": stats,
        "all_tags": all_tags,
        "recent": recent,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "area_labels": AREA_LABELS,
        "area_aliases": AREA_ALIASES,
        "area_order": AREA_ORDER,
    }


# ─────────────────────────── Jinja2 模板 ───────────────────────────

TEMPLATE_INDEX = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>知识库总览</title>
<style>
:root {
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
  --tag-bg: #1f2937; --tag-text: #9ca3af;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: var(--bg); color: var(--text); line-height: 1.6; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ─ Header ─ */
header { border-bottom: 1px solid var(--border); padding: 24px 40px;
         display: flex; align-items: center; justify-content: space-between; }
header h1 { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
header .meta { color: var(--muted); font-size: 13px; }

/* ─ Nav ─ */
nav { padding: 0 40px; border-bottom: 1px solid var(--border);
      display: flex; gap: 4px; flex-wrap: wrap; padding-top: 16px; padding-bottom: 16px; }
nav a { padding: 6px 14px; border-radius: 6px; color: var(--muted); font-size: 14px;
        transition: all 0.15s; }
nav a:hover { background: var(--surface); color: var(--text); text-decoration: none; }
nav a.active { background: var(--surface); color: var(--accent); }

/* ─ Layout ─ */
.container { max-width: 1200px; margin: 0 auto; padding: 40px 40px; }

/* ─ Stats ─ */
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
         gap: 12px; margin-bottom: 40px; }
.stat-card { background: var(--surface); border: 1px solid var(--border);
             border-radius: 8px; padding: 16px; }
.stat-card .num { font-size: 28px; font-weight: 700; color: var(--accent); }
.stat-card .label { font-size: 12px; color: var(--muted); margin-top: 2px; }

/* ─ Area sections ─ */
.area-section { margin-bottom: 48px; }
.area-section h2 { font-size: 16px; font-weight: 600; margin-bottom: 16px;
                   color: var(--muted); text-transform: uppercase;
                   letter-spacing: 1px; border-bottom: 1px solid var(--border);
                   padding-bottom: 8px; }

/* ─ Page grid ─ */
.page-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }
.page-card { background: var(--surface); border: 1px solid var(--border);
             border-radius: 8px; padding: 16px; transition: border-color 0.15s; }
.page-card:hover { border-color: var(--accent); }
.page-card .type-badge { font-size: 11px; color: var(--accent); text-transform: uppercase;
                          letter-spacing: 0.5px; margin-bottom: 6px; }
.page-card h3 { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.page-card h3 a { color: var(--text); }
.page-card h3 a:hover { color: var(--accent); text-decoration: none; }
.page-card .desc { font-size: 13px; color: var(--muted); margin-bottom: 8px;
                   display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.page-card .tags { display: flex; flex-wrap: wrap; gap: 4px; }
.tag { background: var(--tag-bg); color: var(--tag-text); font-size: 11px;
       padding: 2px 8px; border-radius: 4px; }
.page-card .date { font-size: 11px; color: var(--muted); margin-top: 8px; }

/* ─ Recent ─ */
.recent-list { background: var(--surface); border: 1px solid var(--border);
              border-radius: 8px; overflow: hidden; }
.recent-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px;
                border-bottom: 1px solid var(--border); }
.recent-item:last-child { border-bottom: none; }
.recent-item .type { font-size: 11px; color: var(--accent); min-width: 60px; }
.recent-item h4 { flex: 1; font-size: 14px; }
.recent-item .date { font-size: 12px; color: var(--muted); white-space: nowrap; }
.recent-item:hover { background: rgba(88,166,255,0.05); }

/* ─ Tag cloud ─ */
.tag-cloud { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 40px; }
.tag-cloud a { background: var(--tag-bg); color: var(--tag-text); font-size: 13px;
               padding: 4px 12px; border-radius: 6px; transition: all 0.15s; }
.tag-cloud a:hover { background: var(--accent); color: var(--bg); text-decoration: none; }

/* ─ Footer ─ */
footer { border-top: 1px solid var(--border); padding: 24px 40px;
         color: var(--muted); font-size: 12px; margin-top: 60px; }
</style>
</head>
<body>

<header>
  <h1>📚 知识库总览</h1>
  <span class="meta">生成于 {{ generated_at }}</span>
</header>

<nav>
  <a href="/" class="active">总览</a>
  {% for area in area_order %}
  <a href="/area/{{ area_aliases[area] }}/">{{ area_labels[area] }}</a>
  {% endfor %}
</nav>

<div class="container">

  <!-- 统计 -->
  <div class="stats">
    <div class="stat-card">
      <div class="num">{{ pages|length }}</div>
      <div class="label">总页面数</div>
    </div>
    {% for area in area_order %}
    <div class="stat-card">
      <div class="num">{{ stats.get(area, 0) }}</div>
      <div class="label">{{ area_labels[area] }}</div>
    </div>
    {% endfor %}
  </div>

  <!-- 最近更新 -->
  <div class="area-section">
    <h2>🕐 最近更新</h2>
    <div class="recent-list">
      {% for p in recent %}
      <div class="recent-item">
        <span class="type">{{ p.type_label }}</span>
        <h4><a href="{{ p.url }}">{{ p.title }}</a></h4>
        <span class="date">{{ p.updated or p.created }}</span>
      </div>
      {% endfor %}
    </div>
  </div>

  <!-- 各 area 页面 -->
  {% for area in area_order %}
  {% if by_area.get(area) %}
  <div class="area-section">
    <h2>{{ area_labels[area] }} ({{ stats[area] }})</h2>
    <div class="page-grid">
      {% for p in by_area[area] %}
      <div class="page-card">
        <div class="type-badge">{{ p.type_label }}</div>
        <h3><a href="{{ p.url }}">{{ p.title }}</a></h3>
        <p class="desc">{{ p.description }}</p>
        <div class="tags">
          {% for tag in p.tags %}<span class="tag">{{ tag }}</span>{% endfor %}
        </div>
        <div class="date">{{ p.updated or p.created }}</div>
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}
  {% endfor %}

  <!-- 标签云 -->
  {% if all_tags %}
  <div class="tag-cloud">
    {% for tag in all_tags %}
    <a href="/tag/{{ tag }}.html">{{ tag }}</a>
    {% endfor %}
  </div>
  {% endif %}

</div>

<footer>
  由金助理自动化生成 · Obsidian Vault · {{ pages|length }} 个页面
</footer>

</body>
</html>
"""

TEMPLATE_PAGE = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }} — 知识库</title>
<style>
:root {
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
  --tag-bg: #1f2937; --tag-text: #9ca3af;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: var(--bg); color: var(--text); line-height: 1.7; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ─ Header ─ */
header { border-bottom: 1px solid var(--border); padding: 20px 40px;
         display: flex; align-items: center; gap: 16px; }
.breadcrumb { font-size: 13px; color: var(--muted); }
.breadcrumb a { color: var(--muted); }
.breadcrumb a:hover { color: var(--accent); text-decoration: none; }
header h1 { font-size: 18px; font-weight: 700; }

/* ─ Layout ─ */
.layout { display: flex; max-width: 1100px; margin: 0 auto; padding: 32px 40px; gap: 40px; }

/* ─ Sidebar ─ */
.sidebar { width: 220px; flex-shrink: 0; }
.sidebar-box { background: var(--surface); border: 1px solid var(--border);
              border-radius: 8px; padding: 16px; margin-bottom: 16px; font-size: 13px; }
.sidebar-box h3 { font-size: 11px; color: var(--muted); text-transform: uppercase;
                  letter-spacing: 0.5px; margin-bottom: 10px; }
.meta-row { display: flex; justify-content: space-between; padding: 3px 0;
            border-bottom: 1px solid rgba(48,54,61,0.5); }
.meta-row:last-child { border-bottom: none; }
.meta-row .label { color: var(--muted); }
.meta-row .val { color: var(--text); }
.tag { display: inline-block; background: var(--tag-bg); color: var(--tag-text);
       font-size: 11px; padding: 2px 8px; border-radius: 4px; margin: 2px; }
.tags { margin-top: 4px; }

/* ─ TOC ─ */
.toc { background: var(--surface); border: 1px solid var(--border);
       border-radius: 8px; padding: 16px; margin-bottom: 16px; font-size: 13px; }
.toc h3 { font-size: 11px; color: var(--muted); text-transform: uppercase;
          letter-spacing: 0.5px; margin-bottom: 10px; }
.toc-item { padding: 3px 0; }
.toc-item.l2 { padding-left: 12px; }
.toc-item.l3 { padding-left: 24px; }
.toc-item a { color: var(--muted); }
.toc-item a:hover { color: var(--accent); text-decoration: none; }

/* ─ Related ─ */
.related-item { padding: 4px 0; }
.related-item a { color: var(--muted); font-size: 13px; }
.related-item a:hover { color: var(--accent); text-decoration: none; }

/* ─ Sources ─ */
.source-item { padding: 4px 0; font-size: 12px; color: var(--muted); }

/* ─ Main ─ */
.main { flex: 1; min-width: 0; }

/* ─ Article ─ */
.article { background: var(--surface); border: 1px solid var(--border);
           border-radius: 8px; padding: 32px; }
.article h1 { font-size: 22px; font-weight: 700; margin-bottom: 8px;
              border-bottom: 1px solid var(--border); padding-bottom: 16px; }
.article-meta { font-size: 12px; color: var(--muted); margin-bottom: 24px; }

/* ─ MD styles ─ */
.article h2 { font-size: 18px; font-weight: 600; margin: 28px 0 12px;
               border-left: 3px solid var(--accent); padding-left: 10px; }
.article h3 { font-size: 15px; font-weight: 600; margin: 20px 0 10px; color: #c9d1d9; }
.article h4 { font-size: 14px; font-weight: 600; margin: 16px 0 8px; }
.article p { margin-bottom: 14px; color: #c9d1d9; }
.article ul, .article ol { margin: 0 0 14px 20px; color: #c9d1d9; }
.article li { margin-bottom: 4px; }
.article blockquote { border-left: 3px solid var(--accent); padding: 8px 16px;
                       margin: 16px 0; background: rgba(88,166,255,0.05);
                       border-radius: 0 4px 4px 0; color: var(--muted); }
.article table { width: 100%; border-collapse: collapse; margin: 16px 0;
                 font-size: 14px; }
.article th, .article td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
.article th { background: rgba(88,166,255,0.08); color: var(--accent); }
.article td { color: #c9d1d9; }
.article tr:hover td { background: rgba(88,166,255,0.03); }
.article code { background: rgba(88,166,255,0.1); color: #79c0ff;
                padding: 1px 5px; border-radius: 4px; font-size: 13px; font-family: 'Fira Code', monospace; }
.article pre { background: #0d1117; border: 1px solid var(--border); border-radius: 6px;
               padding: 16px; overflow-x: auto; margin: 16px 0; }
.article pre code { background: none; padding: 0; color: var(--text); }
.article img { max-width: 100%; border-radius: 6px; margin: 12px 0; }
.article a { color: var(--accent); }
.article hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
.article .wikilink { color: #79c0ff; background: rgba(88,166,255,0.1);
                     padding: 0 4px; border-radius: 3px; }

/* ─ Footer nav ─ */
.page-nav { display: flex; justify-content: space-between; margin-top: 24px;
            padding-top: 16px; border-top: 1px solid var(--border); font-size: 13px; }
.page-nav a { color: var(--muted); }
.page-nav a:hover { color: var(--accent); text-decoration: none; }

/* ─ Footer ─ */
footer { border-top: 1px solid var(--border); padding: 20px 40px;
         color: var(--muted); font-size: 12px; margin-top: 40px; }

@media (max-width: 768px) {
  .layout { flex-direction: column; padding: 16px; }
  .sidebar { width: 100%; }
}
</style>
</head>
<body>

<header>
  <div class="breadcrumb">
    <a href="/">知识库</a>
    &nbsp;/&nbsp;
    <a href="/area/{{ area_slug }}/">{{ area_label }}</a>
    &nbsp;/&nbsp;
    <span>{{ type_label }}</span>
  </div>
  <h1>{{ title }}</h1>
</header>

<div class="layout">

  <!-- Sidebar -->
  <aside class="sidebar">

    <div class="sidebar-box">
      <h3>页面信息</h3>
      <div class="meta-row"><span class="label">类型</span><span class="val">{{ type_label }}</span></div>
      {% if created %}
      <div class="meta-row"><span class="label">创建</span><span class="val">{{ created }}</span></div>
      {% endif %}
      {% if updated %}
      <div class="meta-row"><span class="label">更新</span><span class="val">{{ updated }}</span></div>
      {% endif %}
      {% if confidence %}
      <div class="meta-row"><span class="label">可信度</span><span class="val">{{ confidence }}</span></div>
      {% endif %}
      {% if tags %}
      <div class="tags" style="margin-top:8px">
        {% for tag in tags %}<span class="tag">{{ tag }}</span>{% endfor %}
      </div>
      {% endif %}
    </div>

    {% if headings %}
    <div class="toc">
      <h3>目录</h3>
      {% for level, title, anchor in headings %}
      <div class="toc-item l{{ level }}"><a href="#{{ anchor }}">{{ title }}</a></div>
      {% endfor %}
    </div>
    {% endif %}

    {% if related %}
    <div class="sidebar-box">
      <h3>相关页面</h3>
      {% for r in related %}
      <div class="related-item"><a href="#">{{ r }}</a></div>
      {% endfor %}
    </div>
    {% endif %}

    {% if sources %}
    <div class="sidebar-box">
      <h3>来源</h3>
      {% for s in sources %}<div class="source-item">{{ s }}</div>{% endfor %}
    </div>
    {% endif %}

  </aside>

  <!-- Main content -->
  <main class="main">
    <div class="article">
      <h1>{{ title }}</h1>
      <div class="article-meta">{{ type_label }} · {{ area_label }}{% if updated %} · 更新于 {{ updated }}{% endif %}</div>
      <div class="content">
        {{ html_body }}
      </div>
    </div>

    <div class="page-nav">
      <span>&nbsp;</span>
      <a href="/area/{{ area_slug }}/">← 返回 {{ area_label }}</a>
    </div>
  </main>

</div>

<footer>
  <a href="/">知识库总览</a> · {{ title }} · 由金助理生成
</footer>

<script>
// 相关页面跳转（本地 wikilinks 修复）
document.querySelectorAll('.related-item a').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    const title = this.textContent.trim();
    // 模糊匹配目标页面
    const allLinks = document.querySelectorAll('.page-card h3 a');
    // 简单降级：直接跳转首页搜索
    window.location.href = '/?q=' + encodeURIComponent(title);
  });
});
</script>

</body>
</html>
"""

TEMPLATE_AREA = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ area_label }} — 知识库</title>
<style>
:root {
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
  --tag-bg: #1f2937; --tag-text: #9ca3af;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: var(--bg); color: var(--text); line-height: 1.6; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
header { border-bottom: 1px solid var(--border); padding: 20px 40px;
         display: flex; align-items: center; gap: 16px; }
.breadcrumb { font-size: 13px; color: var(--muted); }
.breadcrumb a { color: var(--muted); }
.breadcrumb a:hover { color: var(--accent); text-decoration: none; }
header h1 { font-size: 20px; font-weight: 700; }
nav { padding: 0 40px; border-bottom: 1px solid var(--border);
      display: flex; gap: 4px; padding-top: 16px; padding-bottom: 16px; }
nav a { padding: 6px 14px; border-radius: 6px; color: var(--muted); font-size: 14px; }
nav a:hover { background: var(--surface); color: var(--text); text-decoration: none; }
nav a.active { background: var(--surface); color: var(--accent); }
.container { max-width: 1100px; margin: 0 auto; padding: 32px 40px; }
.page-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }
.page-card { background: var(--surface); border: 1px solid var(--border);
             border-radius: 8px; padding: 16px; transition: border-color 0.15s; }
.page-card:hover { border-color: var(--accent); }
.type-badge { font-size: 11px; color: var(--accent); text-transform: uppercase;
              letter-spacing: 0.5px; margin-bottom: 6px; }
.page-card h3 { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.page-card h3 a { color: var(--text); }
.page-card h3 a:hover { color: var(--accent); text-decoration: none; }
.desc { font-size: 13px; color: var(--muted); margin-bottom: 8px;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.tags { display: flex; flex-wrap: wrap; gap: 4px; }
.tag { background: var(--tag-bg); color: var(--tag-text); font-size: 11px;
       padding: 2px 8px; border-radius: 4px; }
.date { font-size: 11px; color: var(--muted); margin-top: 8px; }
.type-filter { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.filter-btn { padding: 6px 14px; border-radius: 6px; font-size: 13px;
              background: var(--surface); border: 1px solid var(--border); color: var(--muted);
              cursor: pointer; transition: all 0.15s; }
.filter-btn:hover, .filter-btn.active { border-color: var(--accent); color: var(--accent); }
footer { border-top: 1px solid var(--border); padding: 20px 40px;
         color: var(--muted); font-size: 12px; margin-top: 40px; }
</style>
</head>
<body>

<header>
  <div class="breadcrumb"><a href="/">知识库</a> &nbsp;/&nbsp;</div>
  <h1>{{ area_label }}</h1>
</header>

<nav>
  <a href="/">总览</a>
  {% for a in area_order %}
  <a href="/area/{{ area_aliases[a] }}/" {% if a == area %}class="active"{% endif %}>{{ area_labels[a] }}</a>
  {% endfor %}
</nav>

<div class="container">
  <div class="type-filter">
    <button class="filter-btn active" data-type="all">全部</button>
    <button class="filter-btn" data-type="entity">实体</button>
    <button class="filter-btn" data-type="concept">概念</button>
    <button class="filter-btn" data-type="sop">流程</button>
    <button class="filter-btn" data-type="raw">原始</button>
  </div>
  <div class="page-grid" id="page-grid">
    {% for p in pages %}
    <div class="page-card" data-type="{{ p.type }}">
      <div class="type-badge">{{ p.type_label }}</div>
      <h3><a href="{{ p.url }}">{{ p.title }}</a></h3>
      <p class="desc">{{ p.description }}</p>
      <div class="tags">{% for t in p.tags %}<span class="tag">{{ t }}</span>{% endfor %}</div>
      <div class="date">{{ p.updated or p.created }}</div>
    </div>
    {% endfor %}
  </div>
</div>

<footer>
  <a href="/">知识库总览</a> · {{ area_label }} · {{ pages|length }} 个页面
</footer>

<script>
const btns = document.querySelectorAll('.filter-btn');
const cards = document.querySelectorAll('.page-card');
btns.forEach(btn => {
  btn.addEventListener('click', () => {
    btns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const type = btn.dataset.type;
    cards.forEach(c => {
      c.style.display = (!type || type === 'all' || c.dataset.type === type) ? '' : 'none';
    });
  });
});
</script>

</body>
</html>
"""

TEMPLATE_TAG = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>#{{ tag }} — 知识库</title>
<style>
:root {
  --bg: #0d1117; --surface: #161b22; --border: #30363d;
  --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
  --tag-bg: #1f2937; --tag-text: #9ca3af;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: var(--bg); color: var(--text); line-height: 1.6; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
header { border-bottom: 1px solid var(--border); padding: 20px 40px; }
header h1 { font-size: 20px; font-weight: 700; }
header span { color: var(--muted); font-size: 14px; margin-left: 8px; }
nav { padding: 0 40px; border-bottom: 1px solid var(--border);
      display: flex; gap: 4px; padding-top: 16px; padding-bottom: 16px; }
nav a { padding: 6px 14px; border-radius: 6px; color: var(--muted); font-size: 14px; }
nav a:hover { background: var(--surface); color: var(--text); text-decoration: none; }
nav a.active { background: var(--surface); color: var(--accent); }
.container { max-width: 1100px; margin: 0 auto; padding: 32px 40px; }
.page-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }
.page-card { background: var(--surface); border: 1px solid var(--border);
             border-radius: 8px; padding: 16px; transition: border-color 0.15s; }
.page-card:hover { border-color: var(--accent); }
.type-badge { font-size: 11px; color: var(--accent); text-transform: uppercase;
              letter-spacing: 0.5px; margin-bottom: 6px; }
.page-card h3 { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.page-card h3 a { color: var(--text); }
.page-card h3 a:hover { color: var(--accent); text-decoration: none; }
.desc { font-size: 13px; color: var(--muted); margin-bottom: 8px;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.tags { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px; }
.tag { background: var(--tag-bg); color: var(--tag-text); font-size: 11px;
       padding: 2px 8px; border-radius: 4px; }
footer { border-top: 1px solid var(--border); padding: 20px 40px;
         color: var(--muted); font-size: 12px; margin-top: 40px; }
</style>
</head>
<body>
<header><h1>#{{ tag }}<span>— 标签页面</span></h1></header>
<nav>
  <a href="/">总览</a>
  {% for a in area_order %}
  <a href="/area/{{ area_aliases[a] }}/">{{ area_labels[a] }}</a>
  {% endfor %}
</nav>
<div class="container">
  <div class="page-grid">
    {% for p in pages %}
    <div class="page-card">
      <div class="type-badge">{{ p.type_label }}</div>
      <h3><a href="{{ p.url }}">{{ p.title }}</a></h3>
      <p class="desc">{{ p.description }}</p>
      <div class="tags">{% for t in p.tags %}<span class="tag">{{ t }}</span>{% endfor %}</div>
    </div>
    {% endfor %}
  </div>
</div>
<footer><a href="/">知识库总览</a> · {{ pages|length }} 个相关页面</footer>
</body>
</html>
"""


# ─────────────────────────── 生成 ───────────────────────────

def write_template(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_site(vault: Path, output: Path):
    print(f"📖 扫描 vault: {vault}")
    pages = read_all_pages(vault)
    print(f"   找到 {len(pages)} 个页面")
    if not pages:
        print("⚠️  未找到任何页面，请检查 vault 路径")
        return

    data = build_site_data(pages)
    output.mkdir(parents=True, exist_ok=True)

    # 1. index.html
    print("🏠 生成 index.html …")
    from jinja2 import Template
    tpl = Template(TEMPLATE_INDEX)
    write_template(output / "index.html", tpl.render(**data))

    # 2. area pages
    for area, area_pages in data["by_area"].items():
        area_slug = AREA_ALIASES.get(area, area)
        area_dir = output / "area" / area_slug
        area_dir.mkdir(parents=True, exist_ok=True)
        print(f"   📂 {area} → {area_slug}/")
        tpl = Template(TEMPLATE_AREA)
        write_template(area_dir / "index.html",
                       tpl.render(area=area, area_label=AREA_LABELS[area],
                                  area_slug=area_slug, pages=area_pages,
                                  area_order=AREA_ORDER,
                                  area_labels=AREA_LABELS,
                                  area_aliases=AREA_ALIASES))

        # 3. 独立页面
        for p in area_pages:
            # 跳过纯原始文件、raw 目录、index、log
            if p["type"] in ("raw", "index", "log") or "/raw/" in p["path"]:
                continue
            page_dir = area_dir
            type_subdir = TYPE_SUBDIR.get(p["type"])
            if type_subdir:
                page_dir = page_dir / type_subdir / p["basename"]
            page_dir.mkdir(parents=True, exist_ok=True)
            page_file = page_dir / f"{p['basename']}.html"
            tpl = Template(TEMPLATE_PAGE)
            write_template(page_file, tpl.render(**p))

    # 3. tag pages（全站一起生成）
    all_tags_data = defaultdict(list)
    for p in pages:
        for t in p.get("tags", []):
            all_tags_data[t].append(p)
    for tag, tag_pages in all_tags_data.items():
        tag_file = output / "tag" / f"{tag}.html"
        tag_file.parent.mkdir(parents=True, exist_ok=True)
        tpl = Template(TEMPLATE_TAG)
        write_template(tag_file,
                        tpl.render(tag=tag, pages=tag_pages,
                                   area_order=AREA_ORDER,
                                   area_labels=AREA_LABELS,
                                   area_aliases=AREA_ALIASES))

    print(f"\n✅ 站点已生成: {output}")
    print(f"   📄 {len(pages)} 个页面")
    print(f"   🏷️  {len(all_tags_data)} 个标签页")
    print(f"\n   本地预览: file://{output}/index.html")
    print(f"   内网预览: http://{HOST}:{PORT}/ (需启动 HTTP 服务)")


# ─────────────────────────── 简易 HTTP 服务器 ───────────────────────────

def run_server(output: Path, host: str, port: int):
    import http.server
    import socketserver
    os.chdir(output)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((host, port), handler) as httpd:
        print(f"\n🌐 知识库站点已启动: http://{host}:{port}/")
        print(f"   按 Ctrl+C 停止")
        httpd.serve_forever()


# ─────────────────────────── CLI ───────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Obsidian 静态站点生成器")
    parser.add_argument("--vault", default=str(VAULT_DIR), help="Vault 路径")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="输出目录")
    parser.add_argument("--host", default=HOST, help="监听地址")
    parser.add_argument("--port", type=int, default=PORT, help="监听端口")
    parser.add_argument("--serve", action="store_true", help="生成后启动 HTTP 服务")
    args = parser.parse_args()

    vault = Path(args.vault)
    output = Path(args.output)

    if not vault.exists():
        print(f"❌ Vault 不存在: {vault}")
        sys.exit(1)

    generate_site(vault, output)

    if args.serve:
        run_server(output, args.host, args.port)


if __name__ == "__main__":
    main()
