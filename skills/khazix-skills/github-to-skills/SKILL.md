---
name: github-to-skills
description: 自动化将GitHub仓库转换为专用AI技能的工厂工具
---

# github-to-skills

## 功能
将任意GitHub仓库转换为标准化的AI技能。

## 特性
- 获取仓库元数据（README、最新提交哈希）
- 创建标准化的技能目录结构
- 生成带frontmatter的`SKILL.md`
- 创建工具调用包装脚本

## 使用方法

```
/github-to-skills <仓库地址>
```

## 示例
```
/github-to-skills https://github.com/yt-dlp/yt-dlp
```

## 执行流程

1. **获取元数据** - 克隆仓库，提取README和提交哈希
2. **创建目录结构** - 生成标准化技能目录
3. **生成SKILL.md** - 包含name、description、usage等frontmatter
4. **生成脚本** - 可选的Python包装脚本

## 输出结构
```
skill-name/
├── SKILL.md
├── scripts/
│   └── ...
└── references/
    └── ...
```
