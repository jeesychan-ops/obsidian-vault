---
title: COSMO 算法
created: 2026-05-25
updated: 2026-05-25
type: entity
tags: [A10算法, 算法, 站内流量]
sources: [raw/articles/2026-05-02-四维协同-A9A10COSMO_Rufus.md]
related: [[A9A10算法]] [[Rufus购物助手]] [[四维算法协同体系]] [[站内流量]]
confidence: high
---

# COSMO 算法

## 什么是 COSMO

COSMO（Commerce OS MOdel）是亚马逊基于大语言模型的新一代搜索推荐算法，2024 年起逐步替代部分 A10 逻辑，核心改变是：**从「关键词匹配」转向「用户意图理解」**。

## 与 A9/A10 的核心区别

| 维度 | A9/A10 | COSMO |
|------|--------|-------|
| 匹配逻辑 | 关键词相关性 | 用户真实意图理解 |
| 排序依据 | CTR + CVR + 转化 | 用户画像 + 场景匹配 |
| 搜索词 | 大词 + 长尾词 | 场景词 + 人群词 |
| 核心问题 | 这个词和产品相关吗？ | 这个人是不是对的人？ |

## COSMO 的流量类型

COSMO 主要驱动以下流量位：

1. **场景化搜索结果** — "running shoes for flat feet"、"yoga mat for hot yoga non slip"
2. **个性化推荐** — 基于用户历史购买/浏览的千人千面推荐
3. **互补品关联** — 买了 X 的用户还买了 Y
4. **场景化问答推荐** — 通过 QA 内容触发的搜索

## COSMO 时代的 Listing 优化策略

### 埋词逻辑变化
- 旧逻辑：关键词密度 = 出现次数
- 新逻辑：**语义完整度** = 是否完整回答"这是什么、适合谁、解决什么、为什么选你"
- 需要覆盖：使用场景、目标人群、痛点解决、差异化卖点

### 具体操作
1. **五点描述**：每条对应一个场景/人群/痛点，不堆功能词
2. **A+ 内容**：加入使用场景图、对比图、人群图
3. **QA**：植入常见问题的高频场景词（"can I use it for X?"）
4. **Backend Keywords**：补充场景词和人群词

### 场景化关键词布局（案例）
> 瑜伽垫案例：
> - 大词："yoga mat"（CPC $2.5，ACOS 32%）
> - COSMO 场景词："yoga mat for hot yoga non slip"（CPC $1.2，ACOS 18%）
> - COSMO 场景词："thick yoga mat for bad knees"（CPC $1.5，ACOS 22%）

## 与其他算法的协同

COSMO 不是独立运行的，它与 [[A9A10算法]] 和 [[Rufus购物助手]] 共同构成亚马逊搜索生态：
- A9/A10：决定「搜这个词，谁排前面」
- COSMO：决定「这个词背后的真实需求是什么，该推什么产品」
- Rufus：覆盖「还没搜，但被种草了」的用户

详见：[[四维算法协同体系]]

---

## 新增：15种关系类型详解（2026-06-04补充）

> 来源：raw/articles/2026-06-04-阿波罗-COSMO五张官方图拆解.md

COSMO定义了15种关系类型（Relations），核心包括：

| 关系类型 | 说明 | 示例 |
|---------|------|------|
| Used For | 用于什么 | Yoga Mat → Stretching |
| Used For Audience | 适合什么人 | Baby Carrier → New Parents |
| Capable Of | 能够实现什么 | Winter Coat → Provide Warmth |
| Used In Location | 在哪儿使用 | Camping Stove → Outdoors |
| Used On Body | 用于身体部位 | — |

**对运营的意义**：Listing不只描述产品属性，更要主动建立这些关系。标题和A+里写"用于XX场景/适合XX人群/能够解决XX问题" = 直接喂COSMO关系标签。

---

## 新增：搜索路径的根本变化（2026-06-04补充）

> 来源：raw/articles/2026-06-04-阿波罗-COSMO五张官方图拆解.md

传统搜索路径：`关键词 → 商品`

COSMO新路径：`目标 → 任务 → 子任务 → 产品类型 → 属性 → 商品`

**案例**：用户搜索"Camping"
- 系统识别"Camping Activity"
- 推导子任务：露营炊具/露营烹饪配件/露营照明
- 再定位具体商品

**运营动作**：选品时按"目标→任务"层级思考——用户买你的产品是为了完成什么任务，而不仅是"这款产品参数如何"。

---

## 新增：COSMO数据来源与知识生成流程（2026-06-04补充）

> 来源：raw/articles/2026-06-04-阿波罗-COSMO五张官方图拆解.md

**两大数据来源：**
1. **Search-Buy数据** — 用户搜索了什么 + 最终购买了什么
2. **Co-Purchase数据** — 哪些商品经常被同时购买

**知识生成流程：**
```
用户行为数据 → LLM生成潜在知识 → 规则过滤 → 相似度过滤 → 人工审核 → 知识图谱
```

关键：COSMO学习的重点不是商品描述，而是用户行为。因为卖家可以优化文案，但用户行为很难伪造。

案例：数百万用户搜索"孕妇鞋"后购买了防滑鞋 → 系统推断"Pregnant → Require → Slip Resistant"

---

## 新增：COSMO与Rufus/Alexa的关系（2026-06-04补充）

> 来源：raw/articles/2026-06-04-阿波罗-COSMO五张官方图拆解.md

COSMO承担了Rufus/Alexa背后的推理层角色：

1. 用户提问："我怀孕了，想买双舒服的鞋"或"我准备开始露营"
2. COSMO将用户身份、目标、场景和担忧转化为具体商品方案
3. Rufus/Alexa输出答案

案例：用户关心"Baby Safety" → COSMO推理出用户真正关心的是婴儿呼吸安全 → 最终推荐Breathing Detection Monitor（不是监视器本身，而是解决安全问题）

**运营动作**：产品定位要从"卖产品参数"转向"卖问题解决方案"

---

## 来源

- [[2026-05-02-四维协同-A9A10COSMO_Rufus]]
- [[2026-06-04-阿波罗-COSMO五张官方图拆解]]