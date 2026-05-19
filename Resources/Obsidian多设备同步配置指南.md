# Obsidian多设备同步配置指南

适用场景：家里电脑、公司电脑、笔记本，多设备同步笔记

---

## 🎯 前置准备

1. 确保您的公钥已经加到服务器（当前电脑配过就跳过）
2. 服务器IP：`149.88.88.243`
3. SSH端口：`58438`
4. 仓库地址：`/home/Obsidian`

---

## 📋 家庭电脑配置步骤（Windows）

### 第一步：安装必要软件

1. 安装 Git for Windows：https://git-scm.com/download/win
2. 安装 Obsidian：https://obsidian.md/

### 第二步：生成SSH密钥（如果家里电脑还没有）

打开 **Git Bash**（不是CMD！），执行：

```bash
ssh-keygen -t rsa -b 4096
# 一路回车就行，不用设密码
```

### 第三步：把公钥发给金助理添加到服务器

在Git Bash执行：
```bash
cat ~/.ssh/id_rsa.pub
```

把输出的一长串内容（从`ssh-rsa`开头）发给金助理，让他加到服务器的授权列表。

### 第四步：配置SSH免密登录（必做！）

打开目录：`C:\Users\你的用户名\.ssh\`

新建一个文件，名字叫 `config`（**注意没有后缀名**，别存成config.txt！）

内容如下：
```ssh-config
Host 149.88.88.243
    Port 58438
    User root
    IdentityFile C:\Users\你的用户名\.ssh\id_rsa
    PreferredAuthentications publickey
```

⚠️ 把"你的用户名"改成你电脑实际的用户名！

### 第五步：克隆仓库

打开Git Bash，执行：

```bash
git clone ssh://root@149.88.88.243:58438/home/Obsidian D:\Obsidian_知识库
```

（可以把D盘改成其他盘，空间够就行）

### 第六步：Obsidian配置Git插件

1. 打开Obsidian → 打开文件夹作为库 → 选择刚才clone的`Obsidian_知识库`
2. 设置 → 第三方插件 → 关闭安全模式
3. 浏览 → 搜索"Git" → 安装 → 启用
4. Git插件设置：
   - ✅ 自动提交间隔：5分钟
   - ✅ 自动推送：开启
   - ✅ 自动拉取：开启

---

## 🔍 验证是否成功

在Git Bash执行：
```bash
ssh root@149.88.88.243
```

如果不用输密码直接连上了，说明配置成功！

---

## 📝 日常使用

- **只管在Obsidian里写笔记**，Git插件自动5分钟同步一次
- 多设备同时写一般不会冲突，万一冲突了插件会提示选哪个版本
- 想手动同步的时候：在仓库目录右键 → Git Bash Here → 执行 `git pull`

---

## ⚠️ 常见问题

### Q：克隆的时候提示Permission denied？
A：检查config文件的路径和文件名对不对，有没有.txt后缀

### Q：空文件夹clone下来看不到？
A：正常，Git不跟踪空目录，往里面放个文件就有了

### Q：电脑切换怎么同步？
A：打开Obsidian等5分钟，Git插件会自动拉取最新内容

---

**配置时间：5分钟搞定！**
