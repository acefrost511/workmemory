---
name: md2wechat
description: 将每日观点/文章转换为微信公众号编辑器可直接粘贴的HTML（已通过实测验证，样式固定零随机性）。触发关键词：公众号排版html、公众号排版、md转公众号、生成公众号版、微信html、手机预览、每日观点HTML。功能：纯内联style，粘贴到微信公众号编辑器后格式最大程度保留，每次输出样式完全一致。
---

# md2wechat - Markdown 转微信公众号 HTML（实测版）

将文章转换为微信公众号编辑器可直接粘贴的 HTML，基于实测验证（2026-04-04多次实测有效）。

## 核心原则（实测铁律）

微信公众号编辑器会过滤掉大部分CSS，只保留以下属性的inline style：

实测可用：color / font-size / font-weight / text-align / font-style

会被过滤：background-color（div/p上）/ border-left / padding / margin / box-shadow / border-radius / linear-gradient / font-family

因此：所有样式只能围绕"颜色+字号+加粗+斜体"五种属性实现。

## 格式规范（实测有效）

主标题：h1 style="font-size:26px;color:#4A3728;text-align:center;"
副标题/篇名：h2 style="font-size:20px;color:#3D2B1F;"
小节标题：p style="font-size:14px;color:#8B7355;font-weight:bold;"（加粗+颜色区分）

正文：p style="font-size:15px;color:#3D2B1F;line-height:1.9;margin:0 0 12px;"
line-height 写在内联style里（不是外部CSS）

视觉分层（不用CSS，用内容）：
分隔线：hr style="border:none;border-top:1px solid #D4C4A8;margin:20px 0;"
小节标签：用 emoji（▶ 💡）代替色块
序号：中文大写数字（壹贰叁肆伍陆柒）+ 加粗

"我的看法"模块：
用金色/斜体区分：color:#C49A3C;font-weight:bold 做标签
正文用斜体：font-style:italic

## 配色方案（古籍书香风格）

颜色代码（均为16进制，微信验证可用）：
#4A3728  深褐（主标题）
#3D2B1F  深棕（正文）
#9A8B78  灰棕（次要文字）
#8B7355  中棕（章节标签）
#C49A3C  金色（强调/我的看法标签）
#D4C4A8  浅褐（分隔线）
#5C4A3D  浅棕（引用正文）

## 禁止使用的标签/样式

严禁使用，粘贴后会被微信过滤：
div style="background-color:..." （背景色100%过滤）
div style="border-left:..." （左边框100%过滤）
div style="padding:..." （div的padding80%过滤）
div style="box-shadow:..." （阴影100%过滤）
div style="border-radius:..." （圆角100%过滤）
blockquote style="..." （引用块样式会变形）

## 执行流程

Step 1：读取 Markdown 源文件
读取 .daily_viewpoint.md 或陛下指定的 markdown 文件

Step 2：复制模板并替换内容（铁律：样式不得更改）
1. 复制下方「模板代码」，粘贴进write内容
2. 按顺序替换以下内容，不得更改任何style属性：
   YYYY年MM月DD日 → 实际日期
   第N期 → 实际期数
   共M条精选 → 实际篇数
   壹 → 中文大写序号（第几篇用几）
   文章标题 → 篇目标题
   English Title → 英文原标题（中文论文则无此行）
   来源：期刊名 · YYYY年M月 → 实际来源
   正文内容…… → 对应段落正文
   看法正文…… → 我的看法内容
   金句正文…… → 一句话内容

Step 3：保存文件
write <content> /workspace/reports/daily/每日观点_YYYY-MM-DD.html

Step 4：上传 CDN 并交付链接
使用 upload_to_cdn 工具上传，交付链接给陛下

Step 5：告知陛下操作方式
"浏览器打开 → Ctrl+A全选 → Ctrl+C复制 → 粘贴进微信公众平台编辑器"

铁律：模板代码中的所有style属性（颜色/字号/间距/对齐方式）一律不得修改，只允许替换文本内容。

## 模板代码（每次必须原样复制，不得修改样式）

▼ 头部（仅一份，全文件只有这一个头部）
h1 style="font-size:26px;color:#4A3728;text-align:center;margin:0 0 4px;" 每日观点
p style="font-size:14px;color:#9A8B78;text-align:center;margin:0 0 4px;" YYYY年MM月DD日 · 第N期 · 共M条精选
hr style="border:none;border-top:1px solid #D4C4A8;margin:20px 0;"

▼ 每篇结构（每篇用这个结构，篇数×重复）
h2 style="font-size:20px;color:#3D2B1F;margin:0 0 4px;" 壹 · 文章标题
p style="font-size:13px;color:#888;font-style:italic;margin:0 0 4px;" English Title（中文论文无此行）
p style="font-size:13px;color:#B8A07A;margin:0 0 14px;" 来源：期刊名 · YYYY年M月
p style="font-size:14px;color:#8B7355;font-weight:bold;margin:0 0 4px;" ▶ 这篇在说什么
p style="font-size:15px;color:#3D2B1F;line-height:1.9;margin:0 0 12px;" 正文内容……
p style="font-size:14px;color:#8B7355;font-weight:bold;margin:0 0 4px;" ▶ 为什么值得你注意
p style="font-size:15px;color:#3D2B1F;line-height:1.9;margin:0 0 12px;" 正文内容……
p style="font-size:14px;color:#C49A3C;font-weight:bold;margin:0 0 4px;" 💡 我的看法
p style="font-size:15px;color:#5C4A3D;line-height:1.9;margin:0 0 12px;font-style:italic;" 看法正文……
p style="font-size:14px;color:#8B7355;font-weight:bold;margin:0 0 4px;" ▶ 如果只记住一句话
p style="font-size:15px;color:#3D2B1F;line-height:1.9;margin:0 0 24px;font-weight:bold;" 金句正文……
hr style="border:none;border-top:1px solid #D4C4A8;margin:20px 0;"

▼ 末篇后附（仅一份）
p style="font-size:13px;color:#C4B89A;text-align:center;" 每日观点 · 转发请注明出处

## 固定样式参数表（禁止随意更改）

主标题 h1 | font-size:26px | color:#4A3728 | text-align:center | margin:0 0 4px
期号行 p | font-size:14px | color:#9A8B78 | text-align:center | margin:0 0 4px
分隔线 hr | border:none | border-top:1px solid #D4C4A8 | margin:20px 0
篇名标题 h2 | font-size:20px | color:#3D2B1F | margin:0 0 4px
英文标题 p | font-size:13px | color:#888 | font-style:italic | margin:0 0 4px
来源 p | font-size:13px | color:#B8A07A | margin:0 0 14px
章节标签 p | font-size:14px | color:#8B7355 | font-weight:bold | margin:0 0 4px
正文 p | font-size:15px | color:#3D2B1F | line-height:1.9 | margin:0 0 12px
我的看法正文 p | font-size:15px | color:#5C4A3D | font-style:italic | line-height:1.9 | margin:0 0 12px
我的看法标签 p | font-size:14px | color:#C49A3C | font-weight:bold | margin:0 0 4px
金句 p | font-size:15px | color:#3D2B1F | font-weight:bold | line-height:1.9 | margin:0 0 24px
底部 p | font-size:13px | color:#C4B89A | text-align:center

## 注意事项

每次只转换一篇每日观点（多篇合一篇）
文件名格式：每日观点_YYYY-MM-DD.html
存储路径：/workspace/reports/daily/
交付方式：先上传CDN，再将链接发给陛下
标题行格式：YYYY年MM月DD日 · 第N期 · 共M条精选（触动二字永久去除）
