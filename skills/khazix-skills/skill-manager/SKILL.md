---
name: skill-manager
description: GitHub技能的生命周期管理器
---

# skill-manager

## 功能
管理已安装GitHub技能的生命周期。

## 特性
- **Audit** - 扫描本地技能文件夹
- **Check** - 比较本地与远程提交哈希
- **Report** - 生成状态报告
- **Update** - 引导式升级技能
- **Inventory** - 列出/删除技能

## 使用方法

```
/skill-manager check          # 扫描更新
/skill-manager list          # 列出所有技能
/skill-manager audit         # 审计技能
/skill-manager report        # 状态报告
/skill-manager delete <name> # 删除技能
```

## 脚本

| 脚本 | 用途 |
|------|------|
| scan_and_check.py | 扫描目录，解析frontmatter，检查远程版本 |
| update_helper.py | 更新前备份文件 |
| list_skills.py | 列出已安装的技能及元数据 |
| delete_skill.py | 永久删除技能 |

## 状态类型
- **Current** - 本地与远程同步
- **Stale** - 远程有新版本
- **Unknown** - 无法检查远程
