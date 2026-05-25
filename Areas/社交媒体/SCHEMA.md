---
title: 社交媒体运营 Wiki Schema
created: 2026-05-25
updated: 2026-05-25
type: schema
owner: SocialBot
---

# 社交媒体运营 Wiki Schema

## 领域范围
小红书运营、公众号运营、内容矩阵、选品种草、KOL/KOC策略、爆款内容结构、数据复盘

## 标签体系

### 平台
- `#小红书` `#公众号`

### 内容类型
- `#选题` `#封面` `#文案` `#标签` `#互动` `#涨粉` `#爆款`

### 标签规则
- 新标签需先写入 SCHEMA.md 再使用

## 命名规范

### 文件名
- 实体页：`平台/账号名.md`（如 `小红书-账号定位.md`）
- 概念页：`概念描述.md`（如 `爆款笔记结构.md`）
- SOP页：`SOP-流程名.md`

### Wikilinks
- 所有页面至少 2 条出站 `[[wikilinks]]`

## Frontmatter 规范

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | SOP
tags: [平台标签, 内容类型标签]
sources: [raw/articles/原始文件名.md]
related: [[目标页1]] [[目标页2]]
confidence: high | medium | low
---
```
