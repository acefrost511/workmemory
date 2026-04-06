---
name: shader-dev
description: |
  GLSL ShaderCraft 技能——36种着色器技术，用于创建令人惊叹的实时视觉效果。
  触发条件：需要光线步进/SDF建模/流体模拟/粒子系统/程序化生成/光照/后处理等视觉效果时。
  兼容：ShaderToy、WebGL2（需适配）。
license: MIT
metadata:
  category: graphics
  version: 1.0
sources:
  - Inigo Quilez (iquilezles.org)
  - ShaderToy
  - GLSL Specification
---

# Shader Craft

36种 GLSL 着色器技术，用于创建实时视觉效果。

## 快速路由表

| 用户想要创建… | 主要技术 | 组合技术 |
|---|---|---|
| 3D物体/场景 | ray-marching + sdf-3d | lighting-model, shadow-techniques |
| 复杂3D形状（布尔运算） | csg-boolean-operations | sdf-3d, ray-marching |
| 无限重复3D图案 | domain-repetition | sdf-3d, ray-marching |
| 有机/变形形状 | domain-warping | procedural-noise |
| 流体/烟雾/墨水效果 | fluid-simulation | multipass-buffer |
| 粒子效果（火花/雪） | particle-system | procedural-noise, color-palette |
| 物理模拟 | simulation-physics | multipass-buffer |
| 海洋/水面 | water-ocean | atmospheric-scattering, lighting-model |
| 地形/景观 | terrain-rendering | atmospheric-scattering, procedural-noise |
| 云/雾/体积火 | volumetric-rendering | procedural-noise, atmospheric-scattering |
| 天空/日落/大气 | atmospheric-scattering | volumetric-rendering |
| 真实感光照（PBR） | lighting-model | shadow-techniques, ambient-occlusion |
| 阴影（软/硬） | shadow-techniques | lighting-model |
| 过程噪声/FBM纹理 | procedural-noise | domain-warping |
| 瓷砖2D图案 | procedural-2d-pattern | polar-uv-manipulation |
| Voronoi/细胞图案 | voronoi-cellular-noise | color-palette |
| 分形（Mandelbrot） | fractal-rendering | color-palette |
| 颜色分级/调色板 | color-palette | — |
| 后处理（Bloom/色调映射） | post-processing | multipass-buffer |
| 多通道 ping-pong 缓冲 | multipass-buffer | — |
| 2D形状/UI来自SDF | sdf-2d | color-palette |

## 技术索引

### 几何与 SDF
- **sdf-2d** — 2D符号距离函数，形状、UI、抗锯齿渲染
- **sdf-3d** — 3D符号距离函数，实时隐式曲面建模
- **csg-boolean-operations** — 构造立体几何：并集、差集、交集、平滑混合
- **domain-repetition** — 无限空间重复、折叠、有限平铺
- **domain-warping** — 用噪声扭曲域，有机流动形状
- **sdf-tricks** — SDF优化、包围盒、二分搜索细化

### 光线投射与光照
- **ray-marching** — 用SDF球体追踪渲染3D场景
- **analytic-ray-tracing** — 解析射线-基元交点（球体、平面、盒子、圆环）
- **path-tracing-gi** — 蒙特卡洛路径追踪全局光照
- **lighting-model** — Phong、Blinn-Phong、PBR (Cook-Torrance)、卡通着色
- **shadow-techniques** — 硬阴影、半影估计、级联阴影
- **ambient-occlusion** — SDF环境光遮蔽
- **normal-estimation** — 有限差分法、四面体技术法线估计

### 模拟与物理
- **fluid-simulation** — Navier-Stokes流体求解器
- **simulation-physics** — GPU物理：弹簧、布料、N体引力、碰撞
- **particle-system** — 无状态和有状态粒子系统（火、雨、火花、星系）
- **cellular-automata** — 生命游戏、反应扩散（图灵斑图）

### 自然现象
- **water-ocean** — Gerstner波、FFT海洋、焦散、水下雾
- **terrain-rendering** — 高度场射线行进、FBM地形
- **atmospheric-scattering** — Rayleigh/Mie散射、神光、SSS近似
- **volumetric-rendering** — 体积射线行进（云、雾、火、爆炸）

### 程序化生成
- **procedural-noise** — Value噪声、Perlin、Simplex、Worley、FBM
- **procedural-2d-pattern** — 砖块、六边形、truchet、伊斯兰几何图案
- **voronoi-cellular-noise** — Voronoi图、Worley噪声、龟裂地面
- **fractal-rendering** — Mandelbrot、Julia集、3D分形

### 后处理与基础设施
- **post-processing** — Bloom、色调映射（ACES, Reinhard）、暗角、色差、故障效果
- **multipass-buffer** — Ping-pong FBO设置、跨帧状态持久化
- **texture-sampling** — 双线性、双三次、Mipmap、过程纹理查询
- **matrix-transform** — 摄像机Look-At、投影、旋转、轨道控制器
- **polar-uv-manipulation** — 极坐标/对数极坐标、万花筒、螺旋映射
- **anti-aliasing** — SSAA、SDF解析AA、时间AA (TAA)
- **camera-effects** — 景深（薄透镜）、运动模糊、镜头畸变、胶片颗粒

### WebGL2 适配规则

ShaderToy 使用 GLSL 风格。生成独立 HTML 页面时应用以下适配：

**Shader 版本与输出：**
```glsl
// 使用 canvas.getContext("webgl2")
// Shader 第一行：#version 300 es
// Fragment 必须声明：out vec4 fragColor;
// Vertex: attribute → in, varying → out
// Fragment: varying → in, gl_FragColor → fragColor
// texture2D() → texture()
```

**Fragment Coordinate：**
```glsl
// 错误
vec2 uv = (2.0 * fragCoord - iResolution.xy) / iResolution.y;
// 正确
vec2 uv = (2.0 * gl_FragCoord.xy - iResolution.xy) / iResolution.y;
```

**main() 包装器（ShaderToy → WebGL2）：**
```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // shader code...
    fragColor = vec4(col, 1.0);
}
void main() {
    mainImage(fragColor, gl_FragCoord.xy);
}
```

**函数声明顺序：** GLSL 要求函数在使用前声明——在使用前定义或重新排序。

**宏限制：** `#define` 不能使用函数调用——使用 `const` 替代。

## 深度参考文件

每个技术文件底部有参考链接，指向 `reference/` 目录下的深度数学推导和高级用法。

关键参考：
- `reference/ray-marching.md` — 步进数学推导与高级模式
- `reference/sdf-3d.md` — 扩展SDF理论
- `reference/lighting-model.md` — 光照数学深度解析
- `reference/procedural-noise.md` — 噪声函数理论
- `reference/webgl-pitfalls.md` — 常见 WebGL2/GLSL 错误
