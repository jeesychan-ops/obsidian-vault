# VPS 迁移恢复指南

## 新 VPS 拿到后执行以下步骤

### 1. 上传备份文件
把 `backup_for_migration_20260520/` 文件夹上传到新 VPS 的 `/root/` 目录

### 2. 安装必要软件
```bash
apt update && apt install -y git cron
```

### 3. 恢复中央仓库
```bash
cd /
tar -xzf /root/backup_for_migration_20260520/01_obsidian_git.tar.gz
```

### 4. 恢复 Obsidian 工作目录
```bash
cd /
tar -xzf /root/backup_for_migration_20260520/02_obsidian_workdir.tar.gz
```

### 5. 恢复 Bot 知识库
```bash
tar -xzf /root/backup_for_migration_20260520/03_bot_knowledge_bases.tar.gz -C /
```

### 6. 恢复同步脚本
```bash
cp /root/backup_for_migration_20260520/04_sync_script.sh /root/sync_knowledge_base.sh
chmod +x /root/sync_knowledge_base.sh
```

### 7. 恢复 Cron 配置
```bash
crontab /root/backup_for_migration_20260520/05_crontab.txt
```

### 8. 恢复 SSH 配置
```bash
cp -r /root/backup_for_migration_20260520/06_ssh_config/* /root/.ssh/
chmod 600 /root/.ssh/*
```

### 9. 配置 post-receive hook（如果没有）
```bash
cat > /git/obsidian.git/hooks/post-receive << 'EOF'
#!/bin/bash
GIT_WORK_TREE=/home/Obsidian git checkout -f master
EOF
chmod +x /git/obsidian.git/hooks/post-receive
```

### 10. 验证
```bash
# 测试同步脚本
bash /root/sync_knowledge_base.sh

# 测试 git 仓库
cd /home/Obsidian
git log --oneline -3
```

## 本地 Windows 连接新 VPS

在新 VPS 上查看 IP 地址，替换 `149.88.88.243` 为新 IP

```powershell
cd E:\Obsidian_知识库
git remote set-url origin ssh://root@新IP:58438/git/obsidian.git
git pull origin master
```

## 备份包清单
- 01_obsidian_git.tar.gz     - 中央仓库
- 02_obsidian_workdir.tar.gz - Obsidian工作目录
- 03_bot_knowledge_bases.tar.gz - Bot知识库
- 04_sync_script.sh          - 同步脚本
- 05_crontab.txt             - Cron定时任务
- 06_ssh_config/            - SSH配置

## 关键路径
- 中央仓库: /git/obsidian.git
- 工作目录: /home/Obsidian
- AmazonBot知识库: /root/.hermes-amazonbot/amazon_knowledge_base
- QuantBot知识库: /root/.hermes-quantbot/quant_knowledge_base
- 同步脚本: /root/sync_knowledge_base.sh
