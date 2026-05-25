---
title: 多Agent共创知识库重构方案
created: 2026-05-25
updated: 2026-05-25
type: summary
tags: [决策记录, 全局]
related: [[多Agent共创知识库重构方案]]
confidence: high
---

# 多Agent共创知识库重构方案

**日期**：2026-05-25
**决策性质**：全局架构决策
**涉及目录**：亚马逊运营/投资-量化/跨境独立站/社交媒体/学习-一建/AI助手对话记录

## 核心决策

### 1. 共享 Vault 方案
- 所有 Bot 共用同一个 Obsidian vault（`~/Obsidian/`）
- 按 Areas 子目录区分业务线，权限边界隔离
- Agents/{botname}/Obsidian/ 保持空白（备用）

### 2. Wiki 三层结构
```
raw/          （原始内容：articles/insights）
  ↓ AI提炼
entities/     （实体：人物/品牌/产品）
concepts/    （概念：方法论/策略/框架）
comparisons/ （对比：方案A vs B）
queries/     （问答：FAQ/选型/诊断）
raw/         （保留原始）
```

### 3. 各 Bot 权限边界
- AmazonBot → `Areas/亚马逊运营/`
- QuantBot → `Areas/投资-量化/`
- WebsiteBot → `Areas/跨境独立站/`
- SocialBot → `Areas/社交媒体/`
- 金助理 → 全 vault（协调者）

### 4. SOUL.md 内嵌知识库策略
- P0 触发关键词自动搜库
- 自动输入整理流程（存raw → AI提炼 → 打标签 → 加wikilinks → 更新index/log）
- 搜不到时的处理策略

### 5. 改造范围（5个业务线）
| 目录 | 改造状态 | Concept页数 |
|------|---------|------------|
| 亚马逊运营 | ✅ 已完成 | 8 |
| 投资-量化 | ✅ 已完成 | 5 |
| 跨境独立站 | ✅ 已完成 | 4 |
| 社交媒体 | ✅ 已完成（空壳） | 0 |
| 学习-一建 | ✅ 已完成 | 2 |
| AI助手对话记录 | ✅ 已完成（空壳） | 0 |

## 来源

- 2026-05-25 金助理与老板对话记录