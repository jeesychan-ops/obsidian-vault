---
title: AI助手对话记录 Wiki Schema
created: 2026-05-25
updated: 2026-05-25
type: schema
owner: 金助理
---

# AI助手对话记录 Wiki Schema

## 领域范围
跨业务线综合分析、老板指令记录、会议纪要、系统配置变更、多Agent协作记录

## 标签体系

### 内容类型
- `#指令` `#配置变更` `#会议纪要` `#跨域分析` `#决策记录`

### 标签规则
- 新标签需先写入 SCHEMA.md 再使用

## 命名规范

### 文件名
- 对话摘要：`对话-YYYYMMDD-HHMM.md`
- 决策记录：`决策-主题-YYYYMMDD.md`
- 配置变更：`配置变更-服务名-YYYYMMDD.md`

### Wikilinks
- 涉及其他业务线的内容加相关链接

## Frontmatter 规范

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: summary | decision | config
tags: [内容类型标签]
related: [[目标页1]]
---
```
