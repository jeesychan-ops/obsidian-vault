---
title: AmazonBot 知识库整理记录
created: 2026-05-25
updated: 2026-05-25
owner: AmazonBot
---

# 知识库整理操作日志

## 2026-05-25 知识库重整

### 问题诊断
- `amazon_kb_structured.json` 共 76 条条目，但按 ID 去重后仅 **31 条独立知识**
- 同一条知识被划入多个话题导致重复计数
- 全部 76 条 source = "未知来源"（公众号名未写入）
- 竞品分析 1 条、评论/QA 1 条，严重不足
- 3 篇独立 JSON 文章（万词打法/四维协同/AMC+Rufus）未整合进 wiki

### 执行操作

#### 骨架层
- [x] `SCHEMA.md` — 补充算法专项标签（#A9算法 #A10算法 #COSMO #Rufus #万词打法），更新话题→Wiki映射关系，新增知识库资产清单
- [x] `log.md` — 本次操作记录

#### Raw 归档层
- [x] 3 篇独立 JSON 原始文章 → `raw/articles/`
  - `2026-05-02-万词打法.md`（来源：炸翻亚马逊！万词打法）
  - `2026-05-02-四维协同-A9A10COSMO_Rufus.md`（来源：亚马逊广告高阶打法）
  - `2026-05-02-AMC_Rufus_Cosmo爆款新玩法.md`（来源：AMC+Rufus+Cosmo+万词打法）
- [x] `amazon_kb_structured.json` 去重版 → `raw/kb/amazon_kb_deduped.json`

#### 新建 Entity 实体页
- [x] `entities/COSMO算法.md` — COSMO 算法实体
- [x] `entities/Rufus购物助手.md` — Rufus AI 购物助手实体
- [x] `entities/A9A10算法.md` — 已有，本次补充 COSMO/Rufus 链接

#### 新建 Concept 概念页
- [x] `concepts/关键词竞争度决策框架.md` — 提炼自 31 条去重知识
- [x] `concepts/万词打法.md` — 提炼自 3 篇独立 JSON 文章
- [x] `concepts/四维算法协同体系.md` — A9+A10+COSMO+Rufus 综合对比

#### 新建 Comparison 对比页
- [x] `comparisons/四大算法对比.md` — A9 vs A10 vs COSMO vs Rufus

#### 新建 Summary 综合页
- [x] `summaries/亚马逊运营全链路摘要.md` — 综合所有来源的运营体系

#### index.md 同步更新
- [x] 更新页面总数（+4 个新页面）
- [x] 补全各类型分类下的所有页面
- [x] 移除"现有知识库资产（未完成Wiki化）"失效标注

### 增量更新（2026-05-25）
- 新抓取：[[2026-05-25-Alexa_for_Shopping_答案位]]（苏乐subi，3552字）
- 新建 Entity： Rufus购物助手.md 补充「Rufus 合并进 Alexa for Shopping」说明
- 新建 Concept： [[Alexa_for_Shopping与答案位]]
- 归档至： raw/articles/2026-05-25-Alexa_for_Shopping_答案位.md
