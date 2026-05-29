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

### 增量更新（2026-05-26）
- 新抓取：[[2026-05-26-悬崖效应-选品工具系统性盲区]]（Sorftime AI Studio，39046字）
  - 核心：硬阈值筛选的悬崖效应，指数排序替代方案，AI工具工程地基四大支柱
  - 新建 entity → entities/2026-05-26-悬崖效应-选品工具系统性盲区.md
- 新抓取：[[2026-05-26-AI时代Amazon高阶选品方法论]]（阿波罗广告增长实战营，7877字）
  - 核心：推广难度六维度公式，算法友好型产品四维模型，未来竞争维度转变
  - 新建 entity → entities/2026-05-26-AI时代Amazon高阶选品方法论.md
- 新抓取：[[2026-05-26-新品上架前准备五模块审定框架]]（亚马逊全流程系统化实战，7877字）
  - 核心：五模块审定框架，预发布九类准备动作，Day -60~Day 0作战地图
  - 新建 entity → entities/2026-05-26-新品上架前准备五模块审定框架.md（文件名保留，title改为"四模块"）
- 归档至： raw/articles/2026-05-26-悬崖效应-选品盲区-Sorftime.md
- 归档至： raw/articles/2026-05-26-AI时代Amazon高阶选品方法论.md
- 归档至： raw/articles/2026-05-26-产品不是死在广告里而是死在上架之前.md
- 按 llm-wiki skill 规范重整：3个raw文件加frontmatter(sha256)，3个entity页补全frontmatter+wikilinks+sources，index.md加入3个新页面，log.md记录本次操作
- index.md 页面总数更新：23 → 26
- index.md 更正：第三篇Module 5（预发布九类准备动作）是课程卖点的列表，没有操作细节，已全部删除；Day -25~-10内容改为简述"预发布准备：Listing+视觉+定价+广告框架预判+用户画像落地"；related中删除SOP-关键词库（该关联是错误添加的）；index.md中删除对SOP-关键词库搭建流程的错误补充说明

### 增量更新（2026-05-26 下半场）— Alexa知识库升级
- 抓取4篇新文章（来源：阿波罗 + 天气指挥家）
  - A9专利（13297字，SHA=c665179fea1161ba）：六种搜索意图类型+搜索路径地图
  - Rufus被Alexa取代（7495字，SHA=ed832383054fc1f8）：对话式购物+AI直接读Listing+价格历史透明化
  - Alexa实操（6524字，SHA=994fe9bc8b234008）：RPO五步法+七天执行清单
  - Alexa升级（14910字，SHA=906eb0a2cba1f872）：80%搜索页AI推荐+五步优化+7天行动清单
- 新建 concepts/：A9搜索意图六分法.md、RPO-推理路径优化.md
- 更新 entities/Rufus购物助手.md：标记deprecated，注明已合并进Alexa for Shopping
- 更新 concepts/Alexa_for_Shopping与答案位.md：追加对话式购物逻辑+Buy for Me+组合关系表达
- 更新 comparisons/四大算法对比.md：Rufus→Alexa for Shopping，更新六列内容，新增外部内容策略行
- 更新 concepts/四维算法协同体系.md：第四维改为Alexa，新增RPO核心策略
- 更新 queries/亚马逊运营高频问题FAQ.md：Q7/Q8 Rufus→Alexa，补充外部内容策略
- 更新 index.md：页面总数26→28，新增两个概念页，Rufus→Alexa标注废弃
- log.md记录本次操作

### 增量更新（2026-05-28）
- 新抓取：[[2026-05-28-广告投放细节-老魏]]（赢商荟-老魏，2274字）
  - 核心：极简化广告策略（新品只开1个自动广告$1竞价$30预算）/ 提竞价50%检验法 / 降广告依赖的售价平衡逻辑 / "排名越靠前价格越敏感"
  - 标签：#广告 #新品冷启动 #竞价策略 #极简化 #运营心法
  - 归档至：raw/articles/2026-05-28-广告投放细节-老魏.md
  - 新建 entity → entities/2026-05-28-老魏极简化广告策略.md
- 新抓取：[[2026-05-28-广告阈值决策-阿波罗]]（阿波罗广告盈利增长实战营，3791字）
  - 核心：三层阈值决策（预警80%/止损100%/淘汰150%）+ 点击20-25次不出单必停 + 高转化词三阶段扩量（加竞价→单独建精准→抢Top of Search）
  - 标签：#广告 #阈值决策 #ACOS诊断 #扩量策略 #算法逻辑
  - 归档至：raw/articles/2026-05-28-广告阈值决策-阿波罗.md
  - 新建 entity → entities/2026-05-28-广告阈值决策体系.md

---

### 增量更新（2026-05-25）
- 新抓取：[[2026-05-25-Alexa_for_Shopping_答案位]]（苏乐subi，3552字）
- 新建 Entity： Rufus购物助手.md 补充「Rufus 合并进 Alexa for Shopping」说明
- 新建 Concept： [[Alexa_for_Shopping与答案位]]
- 归档至： raw/articles/2026-05-25-Alexa_for_Shopping_答案位.md

## 2026-05-28
- 新增: SOP/竞品分析完整SOP (7步竞品分析, 5篇微信文章提炼)
- 来源: 拆解100个对手/可复用判断结构/竞品分析6年老运营/选品3硬指标/2000月销案例
- 抓取: 7篇微信文章 (8个URL含1重复)
- 词库: Garden Tools 10竞品×72关键词飞书文档
