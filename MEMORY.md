# 记忆索引

> 记忆分级管理已迁移至 memory/core/
> 
> 详细规范：memory/core/HEARTBEAT.md
> 索引文件：memory/core/MEMORY.md

---

## 快速跳转

| 级别 | 目录 | 说明 |
|------|------|------|
| L1 | memory/core/ | 核心记忆（永不清理） |
| L2 | memory/business/ | 业务记忆（保留90天） |
| L3 | memory/temp/ | 临时记忆（保留7天） |
| 归档 | memory/archive/ | 压缩归档 |

---

## 最近变更

- [2026-03-08] 建立三级记忆管理体系（L1）
