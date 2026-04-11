---
name: md2wechat 工作流
description: Markdown 转微信公众号 HTML 的标准化流程
type: workflow
updated: 2026-04-04
---

# md2wechat 工作流

## 触发条件

大人发来 Markdown 文档需要排版时，加载本技能生成 HTML。

## 技能文件

- `~/.workbuddy/skills/md2wechat/SKILL.md` — 技能提示词（**v7**）

## 工作流程（重要：AI 直接生成，不依赖脚本）

1. 加载 md2wechat 技能
2. 读取 Markdown 文件内容
3. **AI 直接按 SKILL.md 规范生成 HTML**，将完整 HTML 写入 `.workbuddy/output/` 目录
4. 用 `preview_url` 工具预览 HTML 文件

> ⚠️ 严禁使用 Python 脚本转换。脚本已于 2026-04-04 删除。
> execute_command 跑脚本容易因 API 超时卡住，直接用 AI 生成 HTML 写入文件最稳定。

## v7 设计规范

| 项目 | 规范 |
|------|------|
| 字体族 | `'宋体',SimSun,'STSongti-SC','Songti SC','Noto Serif CJK SC',serif` |
| 标题加粗 | `font-weight:bold`（仅此一项，不使用 stroke/shadow） |
| 正文字重 | `font-weight:400` |
| 加粗 | `font-weight:bold` |
| 代码字体 | `Menlo,Consolas,'Courier New',monospace` |
| 分割线 | `---` → `<hr style="border:none; border-top:1px solid #e0e0e0; margin:32px 0;">` |
| 标题 border | 禁止出现 |
| 外部资源 | 禁止引入任何 CDN、JS、外部 CSS |
| blockquote | 支持多段落（中间空 `>` 行转为 blockquote 内多个 `<p>`，禁止输出 `>` 符号） |

## 设计理念

微信编辑器能实际保留的衬线字体名称，确保粘贴后不降级为黑体。
以 `'宋体',SimSun` 打头，微信编辑器对这两个名字保留率最高。
