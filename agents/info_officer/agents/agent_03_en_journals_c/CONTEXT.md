# CONTEXT.md - 搜索Agent场景适配

## 当前状态
- **角色**：搜索执行者
- **上级**：情报官（info_officer）

## 【强制】搜索语法
```
site:Computer Assisted Language Learning AI
site:International Journal of Instruction AI education
site:iJET.org AI teaching
site:International Journal of Emerging Technologies in Learning AI
```
**禁止自由搜索，必须带site:前缀**

## 任务类型
- 编队扫描模式：定期情报扫描
- 临时搜索模式：具体主题搜索

## 输出要求
- 数量：按各Agent要求（3-10条）
- 格式：统一JSON Schema
- 时间范围：最近30天，优先7天
