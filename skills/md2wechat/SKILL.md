---
name: md2wechat
description: 将 Markdown 文章转换为微信公众号适配的 HTML 网页。触发关键词：公众号排版html、公众号排版、md转公众号、生成公众号版、微信html、手机预览、公众号编辑器。功能：基于纯 HTML + inline styles，无需外部 CSS/JS，粘贴到公众号编辑器即可直接使用，电脑和手机都能预览。
---

# md2wechat - Markdown 转微信公众号 HTML

将 Markdown 文章转换为微信公众号编辑器可直接使用的 HTML 格式，电脑和手机均可预览。

## 核心特点

- **纯 inline styles**：所有样式内联到标签，不依赖外部 CSS
- **公众号兼容**：粘贴到微信公众号编辑器后效果不变形
- **响应式**：电脑浏览器和手机都能正常显示
- **无需安装**：直接用 HTML 模板生成

## 使用方法

### 1. 读取原始 Markdown 文件

```bash
read <path/to/article.md>
```

### 2. 生成微信适配版 HTML

将以下模板中的内容替换为实际文章内容：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>文章标题</title>
</head>
<body style="margin:0;padding:0;background-color:#ffffff;">
<div style="max-width:800px;margin:0 auto;padding:20px 16px 40px;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',Helvetica,sans-serif;font-size:17px;line-height:1.8;color:#333333;">

<!-- 标题 -->
<h1 style="margin:0 0 20px;font-size:24px;font-weight:700;line-height:1.4;color:#1a1a1a;">文章标题</h1>

<!-- 导读（可选） -->
<p style="margin:0 0 30px;font-size:15px;color:#666666;">导读内容...</p>

<!-- 正文段落 -->
<p style="margin:0 0 20px;">正文内容...</p>

<!-- 二级标题 -->
<h2 style="margin:30px 0 16px;font-size:20px;font-weight:700;color:#1a1a1a;border-left:4px solid #007AFF;padding-left:12px;">小标题</h2>

<!-- 加粗重点 -->
<strong>重点内容</strong>

<!-- 引用块 -->
<blockquote style="margin:20px 0;padding:16px;background:#f5f7fa;border-left:4px solid #007AFF;border-radius:4px;">
<p style="margin:0;">引用内容...</p>
</blockquote>

<!-- 总结框 -->
<div style="margin:30px 0;padding:20px;background:linear-gradient(135deg,#f5f7fa,#e4e8ec);border-radius:12px;text-align:center;">
<p style="margin:0;font-size:18px;font-weight:600;color:#1a1a1a;">总结标题</p>
<p style="margin:12px 0 0;font-size:15px;color:#666666;">总结内容...</p>
</div>

<!-- 底部 -->
<div style="margin-top:40px;padding-top:20px;border-top:1px solid #eeeeee;text-align:center;">
<p style="margin:0;font-size:13px;color:#999999;">本文由 K12 AI教育日报 深度解读系列出品</p>
</div>

</div>
</body>
</html>
```

### 3. 保存 HTML 文件

```bash
write <content> /workspace/reports/daily/xxx_wechat.html
```

## 样式规范

### 字体
```css
font-family: -apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',Helvetica,sans-serif;
```

### 正文字号
```css
font-size: 17px;
line-height: 1.8;
```

### 标题字号
- h1: 24px, font-weight: 700
- h2: 20px, font-weight: 700

### 标题颜色
- 主标题: #1a1a1a
- 二级标题左边框: #007AFF (蓝), #34C759 (绿), #FF9500 (橙), #FF3B30 (红)

### 段落间距
- 段前: 0
- 段后: 20px (普通段落), 30px (小节后)

### 特殊样式
- 强调框背景: linear-gradient(135deg,#f5f7fa,#e4e8ec)
- 重点文字: font-weight: 600

## 快捷命令

直接生成微信适配 HTML 的完整流程：

1. 读取 Markdown 源文件
2. 按上述模板格式转换
3. 保存为 `_wechat.html` 后缀的文件
4. 告知用户用浏览器预览，全选复制粘贴到公众号编辑器
