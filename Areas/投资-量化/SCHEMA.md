---
title: 投资-量化 Wiki Schema
created: 2026-05-25
updated: 2026-05-25
type: schema
owner: QuantBot
---

# 投资-量化 Wiki Schema

## 领域范围
A股/美股/港股、可转债、期权、量化策略、基金组合、风控模型、投资心理学、巴菲特价值投资

## 标签体系

### 资产类别
- `#可转债` `#期权` `#A股` `#美股` `#ETF` `#基金` `#期货`

### 策略类型
- `#双低策略` `#困境反转` `#哑铃配置` `#趋势跟踪` `#价值投资` `#量化`

### 分析维度
- `#选股` `#择时` `#风控` `#仓位管理` `#回测` `#财务分析`

### 标签规则
- 每页至少一个资产标签 + 一个策略标签
- 新标签需先写入 SCHEMA.md 再使用

## 命名规范

### 文件名
- 实体页：`标的/策略名.md`（如 `双低可转债.md`、`巴菲特.md`）
- 概念页：`概念描述.md`（如 `仓位管理原则.md`）
- 对比页：`对比A-vs-B.md`
- 复盘页：`周报-YYYY-MM-WW.md`

### Wikilinks
- 所有页面至少 2 条出站 `[[wikilinks]]`
- 链接目标必须存在

## Frontmatter 规范

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | SOP | summary
tags: [资产标签, 策略标签]
sources: [raw/articles/原始文件名.md]
related: [[目标页1]] [[目标页2]]
confidence: high | medium | low
---
```

## 来源追溯
- 来自 json 原始文章的须在 `sources:` 标注
- 多来源综合页面在相关段落加 `^[raw/articles/文件名.json]`

## 更新政策
- 新信息与旧信息冲突时保留两者，标注 `contested: true`
- 重大更新 append 到 `log.md`
