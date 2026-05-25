---
title: 跨境独立站 Wiki Schema
created: 2026-05-25
updated: 2026-05-25
type: schema
owner: WebsiteBot
---

# 跨境独立站 Wiki Schema

## 领域范围
Shopify 建站、SEO / GEO 内容策略、Google Ads / 社媒广告、流量渠道、转化率优化、B2B 询价流程

## 标签体系

### 业务环节
- `#建站` `#SEO` `#GEO` `#广告` `#流量` `#转化` `#社媒`

### 内容类型
- `#策略` `#SOP` `#工具` `#数据` `#案例`

### 标签规则
- 新标签需先写入 SCHEMA.md 再使用

## 命名规范

### 文件名
- 实体页：`平台/工具名.md`（如 `Shopify.md`）
- 概念页：`策略描述.md`（如 `SEO关键词策略.md`）
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
tags: [业务环节标签, 内容类型标签]
sources: [raw/articles/原始文件名.md]
related: [[目标页1]] [[目标页2]]
confidence: high | medium | low
---
```

## 更新政策
- 新信息与旧信息冲突时保留两者，标注 `contested: true`
- 重大更新 append 到 `log.md`
