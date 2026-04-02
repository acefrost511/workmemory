---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 38169029266cce2660a2cac8c3a09fab
    PropagateID: 38169029266cce2660a2cac8c3a09fab
    ReservedCode1: 304502204bc7462e76f1562b9e7ad75195c886f1a852a5d2d1971e46346d0744b6badb1b022100e9926fdb948a8bcc7e7ca00147be7f6813fdd974ca85b6076037b69844fc9f7e
    ReservedCode2: 30450221008e334b6dd1888fa93b510b543eb9c865741fa31f85d67f04392a7eed4ea03bd00220110c80f488ad59bccb324ad53008d67637ab82d230e6f8ab60346a394a19e8a0
description: |
    全栈前端开发技能，精通React/Next.js、Tailwind CSS、Framer Motion、GSAP动画、AIDA文案框架。
    触发条件：构建落地页/动态网页/需要电影级动效的前端项目、需要AI媒体资源（图像/视频/音频/TTS）集成的项目。
    包含：p5.js生成艺术、Three.js/R3F、WebGL、视觉工程规范、运动动画引擎、资产生成工作流。
license: MIT
metadata:
    category: frontend
    version: 1.0.0
name: frontend-dev
sources:
    - Framer Motion Documentation
    - GSAP / GreenSock Documentation
    - Three.js Documentation
    - Tailwind CSS Documentation
    - React / Next.js Documentation
    - AIDA Framework (Elmo Lewis)
    - p5.js Documentation
---

# Frontend Studio

## 核心约束（违反即为阻塞错误）

- **禁止占位图**：禁止使用 unsplash/picsum/placeholder.com 等占位图，所有媒体必须本地生成
- **禁止混用动画库**：同一组件内禁止同时使用 GSAP 和 Framer Motion
- **禁止渐变文字标题**：Gradient text on headers 禁止
- **禁止纯黑背景**：纯黑 (#000) 禁止
- **禁止 Inter 字体**：禁止使用 Inter，改为 Geist/Outfit/Satoshi
- **禁止 emoji**：所有场景下禁止 emoji，使用 Phosphor 或 Radix icons
- **GPU-only 动画属性**：只允许动画 `transform`/`opacity`/`filter`/`clip-path`，禁止动画 `width`/`height`/`font-size`
- **必须响应 `prefers-reduced-motion`**

## 设计刻度盘

| 刻度 | 默认值 | 范围 |
|------|--------|------|
| DESIGN_VARIANCE | 8 | 1=对称, 10=不对称 |
| MOTION_INTENSITY | 6 | 1=静态, 10=电影级 |
| VISUAL_DENSITY | 4 | 1=通透, 10=紧凑 |

## Phase 1：设计架构

1. 分析请求 → 判定页面类型和使用场景
2. 基于页面类型设置设计刻度
3. 规划布局区块，识别资产需求

## Phase 2：运动架构

1. 按区块选择动画工具（见工具选择矩阵）
2. 按性能规范规划运动序列

## Phase 3：资产生成

通过 `scripts/` 生成所有图像/视频/音频。使用 MiniMax API。
生成后必须本地保存，不得使用外部 URL。

## Phase 4：文案撰写

遵循 AIDA/PAS/FAB 框架撰写所有文本内容。禁止 Lorem ipsum。

## Phase 5：构建 UI

脚手架项目，按设计与运动规范构建每个区块，集成生成资产和文案。

## Phase 6：质量门

- [ ] 移动端布局折叠检查（w-full, px-4）
- [ ] 使用 `min-h-[100dvh]` 而非 `h-screen`
- [ ] 提供 Empty/Loading/Error 状态
- [ ] 正确工具选择（工具选择矩阵）
- [ ] 无 GSAP + Framer Motion 混用
- [ ] 所有 useEffect 有 cleanup returns
- [ ] 依赖已验证于 package.json

## 工具选择矩阵

| 需求 | 工具 |
|------|------|
| UI 进入/退出/布局动画 | Framer Motion |
| 滚动叙事（pin/scrub） | GSAP + ScrollTrigger |
| 循环图标 | Lottie（懒加载） |
| 3D/WebGL | Three.js / R3F（独立 Canvas） |
| 悬停/焦点状态 | 纯 CSS |

## 动画强度量表

| 级别 | 技术 |
|------|------|
| 1-2 微 | CSS transition，150-300ms |
| 3-4 流畅 | CSS keyframes + Framer animate，错落 ≤3 项 |
| 5-6 流体 | whileInView、磁性悬停、视差倾斜 |
| 7-8 电影 | GSAP ScrollTrigger、固定区块、横向拦截 |
| 9-10 沉浸 | 全滚动序列、Three.js 粒子、WebGL shader |

## 动画处方

| 处方 | 工具 | 用途 |
|------|------|------|
| 滚动揭示 | Framer | 视口进入时淡入+滑动 |
| 错落网格 | Framer | 顺序列表动画 |
| 固定时间线 | GSAP | 带固定的横向滚动 |
| 倾斜卡片 | Framer | 鼠标追踪3D透视 |
| 磁性按钮 | Framer | 光标吸引按钮 |
| 文本乱码 | Vanilla | Matrix式解码效果 |
| 粒子背景 | R3F | 装饰性WebGL粒子 |

## 性能规则

- GPU-only 属性（只动画这些）：`transform`、`opacity`、`filter`、`clip-path`
- 永远不要动画：`width`、`height`、`top`、`left`、`margin`、`padding`、`font-size`
- 永远动画：`transform: scale()` 或 `clip-path` 替代
- 包含：`layout style paint` 在重型容器上
- 移动端：始终尊重 `prefers-reduced-motion`，始终禁用指针：粗的视差/3D
- 粒子上限：桌面 800，平板 300，手机 100

## 文案框架

**AIDA**（着陆页/邮件）：
- ATTENTION：粗体标题（承诺或痛点）
- INTEREST：详细阐述问题（"是的，就是我"）
- DESIRE：展示转变
- ACTION：明确 CTA

**PAS**（痛点驱动产品）：
- PROBLEM：清晰陈述
- AGITATE：制造紧迫
- SOLUTION：你的产品

## 视觉艺术

两种输出模式：

| 模式 | 输出 | 时机 |
|------|------|------|
| 静态 | PDF/PNG | 海报、印刷、设计资产 |
| 交互 | HTML (p5.js) | 生成艺术、可探索变体 |

## 附加资源

- `/workspace/skills/frontend-dev/references/` — 详细参考指南（按需读取）
- `references/motion-recipes.md` — 动画代码片段处方
- `references/minimax-cli-reference.md` — CLI 标志快速参考
- `references/asset-prompt-guide.md` — 资产提示工程规则
- `references/minimax-voice-catalog.md` — 所有语音 ID
- `references/minimax-tts-guide.md` — TTS 使用与语音
- `references/minimax-music-guide.md` — 音乐提示与歌词格式
- `references/minimax-video-guide.md` — 相机命令与模型
- `references/minimax-image-guide.md` — 比率与批量生成
- `references/env-setup.md` — 环境设置
- `references/troubleshooting.md` — 常见问题

## 模板

- `/workspace/skills/frontend-dev/templates/viewer.html` — p5.js 交互艺术基础
- `/workspace/skills/frontend-dev/templates/generator_template.js` — p5.js 代码参考
- `/workspace/skills/frontend-dev/canvas-fonts/` — 静态艺术字体（TTF + 许可证）
