---
title: 投资-量化 Wiki 操作日志
created: 2026-05-25
updated: 2026-05-25
type: log
owner: QuantBot
---

# Wiki 操作日志

> 格式：`## [日期] action | subject`

---

## [2026-05-25] init | Wiki 结构初始化
- 创建目录：raw/articles/, raw/insights/, entities/, concepts/, comparisons/, queries/, SOP/, raw/weekly/, raw/kb/
- 创建文件：SCHEMA.md, index.md, log.md
- 负责人：金助理（批量改造）

## [2026-05-25] create | 实体页创建
- [[巴菲特]] — 价值投资核心人物，5个核心概念链接
- [[稳盈君]] — 用户画像，含资金现状/资产配置/投资红线

## [2026-05-25] create | 概念页创建
- [[投资理念总纲]] — 巴菲特四大原则（护城河/安全边际/能力圈/市场先生）
- [[双低可转债策略]] — 筛选条件+双低值计算+操作规则+止盈止损
- [[量化策略库]] — 网格/趋势/套利/双低轮动/小市值五策略
- [[投资洞察精华]] — 风险度量/资产配置/逆向思维
- [[仓位管理原则]] — 三层仓原则+软止损+硬止损

## [2026-05-25] create | SOP页创建
- [[每周复盘SOP]] — 持仓检查+双低扫描+市场判断+输出模板

## [2026-05-25] organize | 原始文件归档
- 投资工具箱.md → raw/articles/
- kb_wenying_invest.md → raw/kb/
- 第21周复盘.md → raw/weekly/
- Shopify配置方案.md → raw/articles/
- 关键词研究报告.md → raw/articles/
- 竞品分析报告.md → raw/articles/

## [2026-05-25] merge | 知识库重复内容合并整理
**合并操作：**
- `concepts/投资理念总纲.md` + `仓位管理原则.md` 各自去重，移除重复的三层仓位结构
- `concepts/量化策略库.md` 移除双低可转债详情（已独立成页）
- `entities/稳盈君.md` 只保留用户画像，移除外延策略内容
- `concepts/投资洞察精华.md` 精简策略评级速查表

**归档操作：**
- 迁入根目录 6个散落的 2026-05-19-*.md → `raw/articles/`
- 迁入根目录 `每周复盘/` 目录 → 内容已存 `raw/weekly/`
- 清理 `知识库/kb_wenying_invest.md`（与 `raw/kb/` 重复）
- 清理 `知识库/期权交易实战手册v2.0.md`（与 `raw/kb/` 重复）

## [2026-06-06] create | 板块轮动方法论入库
- **来源**：微信公众号文章「掌握板块轮动节奏的完整方法论」
- **raw 提炼**：[[板块轮动节奏完整方法论-提炼]] → raw/articles/
- **概念页**：[[板块轮动方法论]] → concepts/
- **更新**：index.md 新增索引条目
- **知识库状态**：74篇文章 / 2417条知识条目
- `index.md` — 反映合并后实际页面，添加知识库结构图和日志记录