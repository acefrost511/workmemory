# Khazix-Skills 技能库

## 概述
这是一个用于管理和演进AI技能库的工具集合，包含3个核心技能。

---

## 技能一：github-to-skills

### 描述
自动化将GitHub仓库转换为专用AI技能的工厂工具。

### 功能特性
- 获取仓库元数据（README、最新提交哈希）
- 创建标准化的技能目录结构
- 生成带有生命周期管理扩展frontmatter的`SKILL.md`
- 创建用于工具调用的包装脚本

### 使用方法

/github-to-skills <仓库地址>

### 示例

/github-to-skills https://github.com/yt-dlp/yt-dlp

---

## 技能二：skill-manager

### 描述
GitHub技能的生命周期管理器。

### 功能特性
- **Audit（审计）**: 扫描本地技能文件夹，查找基于GitHub的技能
- **Check（检查）**: 比较本地提交哈希与远程HEAD
- **Report（报告）**: 生成状态报告（Stale/Current）
- **Update（更新）**: 引导式工作流升级技能
- **Inventory（清单）**: 列出所有技能，删除不需要的技能

### 使用方法

/skill-manager check  # 扫描更新
/skill-manager list   # 列出所有技能
/skill-manager delete <skill-name>  # 删除技能

### 脚本列表
| 脚本 | 用途 |
|------|------|
| `scan_and_check.py` | 扫描目录，解析frontmatter，检查远程版本 |
| `update_helper.py` | 更新前备份文件 |
| `list_skills.py` | 列出已安装的技能及元数据 |
| `delete_skill.py` | 永久删除技能 |

---

## 技能三：skill-evolution-manager

### 描述
基于用户反馈和会话洞察持续改进技能。

### 核心概念
1. **Session Review（会话审查）**: 对话后分析技能表现
2. **Experience Extraction（经验提取）**: 将反馈转换为结构化的`evolution.json`
3. **Smart Stitching（智能缝合）**: 将最佳实践持久化到`SKILL.md`

### 使用方法

/evolve

或使用自然语言："Save this experience to the skill"

### 工作流程
1. **Review（审查）**: Agent分析什么有效/无效
2. **Extract（提取）**: 创建包含偏好、修复、自定义提示的结构化JSON
3. **Persist（持久化）**: 合并到`evolution.json`
4. **Stitch（缝合）**: 用学到的最佳实践更新`SKILL.md`

### 脚本列表
| 脚本 | 用途 |
|------|------|
| `merge_evolution.py` | 增量合并新经验数据 |
| `smart_stitch.py` | 生成/更新SKILL.md中的最佳实践部分 |
| `align_all.py` | 批量重新缝合所有技能 |

---

## 完整技能生命周期工作流

```
github-to-skills → skill-manager → skill-evolution-manager
   创建技能          维护更新          基于反馈演进
```

1. **创建（Create）**: 使用`github-to-skills`将GitHub仓库封装为技能
2. **维护（Maintain）**: 使用`skill-manager`检查更新并进行升级
3. **演进（Evolve）**: 使用`skill-evolution-manager`捕获学习成果并改进

---

## 依赖要求
- Python 3.8+
- Git（用于检查远程仓库）
- PyYAML（`pip install pyyaml`）
