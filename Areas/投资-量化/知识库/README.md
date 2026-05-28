# 稳盈君专属量化投资知识库

> **路径**: `/home/ubuntu/agents/quantbot/quant_knowledge_base/`
> **版本**: 2.0（2026-05-02，已同步 Skill 全部内容）
> **访问权限**: 仅限本人，独立于系统通用知识库

---

## 目录结构

```
quant_knowledge_base/
├── kb_wenying_invest.json       ← 核心配置（JSON版，主配置）
├── kb_wenying_invest.md         ← 可读版，快速查阅（推荐）
├── README.md                    ← 本文件
│
├── articles/                   ← 微信文章原文（按日期命名）
│   └── YYYYMMDD_文章标题.json
│
├── insights/insights.json       ← 提炼的投资洞察精华
│
├── strategies/                 ← 策略研究笔记
│   └── strategy_name.md
│
├── portfolios/                 ← 持仓快照存档
│   └── portfolio_YYYYMMDD.json
│
└── weekly_review/              ← 每周复盘记录
    └── review_YYYYWW.md
```

---

## 使用规则

### 文章保存流程
1. 用户发送微信链接
2. 抓取：`python3 /root/.hermes/scripts/wechat_fetch.py --url <链接>`
3. 保存到 `articles/YYYYMMDD_标题.json`
4. 提炼洞察，追加到 `insights/insights.json`
5. 归档结论到 `strategies/` 或更新 `kb_wenying_invest.json`

### 知识库更新时机
| 时机 | 更新位置 |
|------|---------|
| 持仓变动 | `kb_wenying_invest.json` → `portfolio_diagnosis` |
| 策略研究结论 | `strategies/<策略名>.md` |
| 微信文章分析 | `articles/` + `insights/insights.json` + `strategy_archive` |
| 每周复盘 | `weekly_review/review_YYYYWW.md` |
| 月末总结 | `portfolios/portfolio_YYYYMMDD.json` |

---

## 快速导航

| 你想知道 | 看哪个文件 |
|---------|-----------|
| 我的持仓和资金 | `kb_wenying_invest.json` → `portfolio_diagnosis` |
| 我的投资原则 | `kb_wenying_invest.md` 第2-3节 |
| 可转债双低怎么筛 | `kb_wenying_invest.md` 第6节 |
| 分众/海大怎么处理 | `kb_wenying_invest.json` → `portfolio_diagnosis.special_constraints` |
| 晶科科技换什么 | `kb_wenying_invest.md` 第4节"止血优先级" |
| 近期投研洞察 | `insights/insights.json` |
| 策略归档库 | `kb_wenying_invest.json` → `strategy_archive` |
| 微信文章原文 | `articles/` |
| 飞书知识库 | https://xinjiashuma.feishu.cn/base/KhndbEBSRaKsbosrhoqcBUMUn0e |

---

## 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0 | 2026-05-02 | 初始创建，从会话记忆中提取 |
| 2.0 | 2026-05-02 | 同步 Skill（quant-strategy-kb）全部内容，含策略SOP、资产配置、每周复盘模板 |

---

## 系统脚本

| 脚本 | 路径 |
|------|------|
| 持仓诊断 | `~/.hermes-quantbot/scripts/stock_analysis.py` |
| 单股诊断 | `~/.hermes-quantbot/scripts/diagnosis.py` |
| 双低扫描 | `~/.hermes-quantbot/scripts/cb_dual_low_scan.py` |
| 双低回测 | `~/.hermes-quantbot/scripts/cb_dual_low_backtest.py` |
| 微信抓取 | `python3 /root/.hermes/scripts/wechat_fetch.py --url <url>` |
