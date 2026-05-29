---
title: Obsidian + Claude Code AI 工作台
source: 跨境成长圈
date: 2026-05-29
url: https://mp.weixin.qq.com/s/CMJCAW3yy2QCqt5XbWv_Gw
type: concept
tags:
  - Obsidian
  - Claude Code
  - AI工作台
  - 内容创作
  - 效率工具
  - OrbitOS
related_concepts:
  - AI助手对话记录
---

# Obsidian + Claude Code AI 工作台

## 核心定位

用 **Obsidian** 作为本地笔记和资料库，用 **Claude Code** 作为 AI 引擎，自动整理待办、追踪热点、生成选题。

核心价值：**你负责判断方向，AI 负责把零散信息整理成清晰的下一步。**

---

## 核心概念

| 概念 | 含义 |
|------|------|
| Obsidian | 本地笔记软件，文章、项目、灵感都存在里面 |
| Vault | Obsidian 里的资料库，本质是电脑里的一个文件夹 |
| Claude Code | AI 助手，可读取、整理、生成文件内容 |
| Skill | 提前写好的工作流程（如 Start My Day） |
| API Key | 连接 AI 服务的授权码 |
| OrbitOS | Obsidian 模板套件，包含多个现成工作流 |

---

## 五大核心工作流

### 1. Start My Day（每日启动）

**功能**：自动生成今日计划

**AI 自动完成**：
- 回顾昨天日记，找出未完成事项
- 扫描所有项目，提醒快到截止时间的任务
- 检查收件箱里还没处理的想法
- 问你今天最重要的目标是什么
- 整理成一份今日计划

**输出示例**：
```
今日计划
- 优先处理：[昨天未完成的事项]
- 即将到期：[快到截止时间的任务]
- 待推进：[收件箱里的想法]
- 今日目标：[你回答的方向]
```

> 全程不到 3 分钟。

---

### 2. Kickoff（想法 → 项目）

**功能**：把模糊想法拆解为可执行计划

**AI 帮你分析**：
- 这个想法适不适合做成项目
- 可以拆成哪些步骤
- 需要先准备哪些资料
- 下一步最适合做什么

---

### 3. AI Newsletter（热点追踪）

**功能**：自动收集当天 AI 相关热点，筛选与内容方向相关的主题，并生成选题建议，直接写入今日计划

---

### 4. Research（主题研究）

**功能**：帮你整理某个主题的背景信息，形成结构化研究文档

---

### 5. Brainstorm（头脑风暴）

**功能**：针对某个话题进行发散性思考，生成创意方向

---

## 安装方式对比

| 方式 | 适合人群 | 优点 | 注意 |
|------|---------|------|------|
| Claudian 插件 | 新手 | 界面友好，操作像普通软件插件 | 通常用 Claude API，费用可能更高 |
| Terminal + Claude Code | 愿意折腾的人 | 更灵活，可接入其他模型服务 | 需要安装配置 Claude Code |

---

## OrbitOS 安装步骤

1. **下载 OrbitOS 模板**
   ```
   git clone https://github.com/MarsWang42/OrbitOS
   ```
   或从 GitHub 下载并解压，得到 `OrbitOS-vault` 文件夹

2. **在 Obsidian 中打开**
   - 点击"打开文件夹作为仓库"
   - 选择 `OrbitOS-vault` 文件夹
   - 等待加载完成

3. **配置 AI 连接**（二选一）

   **方式一：Claudian 插件**
   - 设置 → 社区插件 → 搜索 Claudian / Agent Client → 安装并启用
   - 进入插件设置页，填入 API Key

   **方式二：Terminal + Claude Code**
   - 设置 → 社区插件市场 → 搜索 Terminal 并安装
   - 在左侧面板右键，选择"在终端开启"，建议选"外部"（整合式有时卡顿）
   - Claude Code 启动后，直接输入工作流名称（如 `Start My Day`）

---

## 快速上手路径

1. 每天早上运行 `Start My Day`，让 AI 帮你整理今日计划
2. 平时把灵感丢进收件箱，不急着整理
3. 某个想法值得推进时，运行 `Kickoff` 把它变成项目
4. 需要查资料时，运行 `Research`
5. 没有选题灵感时，运行 `Brainstorm` 或 `AI Newsletter`

---

## 重要警示

> 当你让 AI 阅读、总结或改写某些内容时，相关内容会发送给配置的 AI 服务商。**敏感资料、账号密码、私人信息，建议不要交给 AI 处理。**

---

## 核心价值总结

Obsidian 负责保存资料，Claude Code 负责整理和推进任务。

这套组合**不是让 AI 取代你思考**，而是帮你把每天零散的信息、待办和想法收拢起来，让你更清楚知道下一步该做什么。

> **先从 Start My Day 开始用。每天早上跑一次，很快就能感受到它对创作节奏的帮助。**