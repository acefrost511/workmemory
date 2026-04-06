---
name: ios-application-dev
description: |
  iOS 应用开发指南，涵盖 UIKit、SwiftUI、SnapKit。
  包括触控目标、安全区域、导航模式、Dynamic Type、深色模式、无障碍访问、
  集合视图、Apple HIG 合规性。
  触发条件：开发 iOS 应用、实现 UI、使用 UIKit/SwiftUI 布局、
  构建 iPhone 界面、Apple HIG 合规检查。
license: MIT
metadata:
  category: mobile
  version: 1.0.0
sources:
  - Apple Human Interface Guidelines
  - Apple Developer Documentation
---

# iOS 应用开发规范

## 布局

- **触控目标 >= 44pt**
- **内容在安全区域内**（SwiftUI 默认遵守，用 `.ignoresSafeArea()` 仅做背景）
- **使用 8pt 间距增量**（8, 16, 24, 32, 40, 48）
- **主要操作在拇指区域**（屏幕下半部分）
- **支持所有屏幕尺寸**（iPhone SE 375pt 到 Pro Max 430pt）

## 排版

- **UIKit**：`preferredFont(forTextStyle:)` + `adjustsFontForContentSizeCategory = true`
- **SwiftUI**：语义文本样式 `.headline`、`.body`、`.caption`
- **自定义字体**：`UIFontMetrics` / `Font.custom(_:size:relativeTo:)`
- **无障碍尺寸下自适应布局**（最小 11pt）

## 色彩

- ✅ 使用语义系统颜色（`.systemBackground`、`.label`、`.primary`）
- ✅ Asset catalog 为自定义颜色提供 Any/Dark Appearance 变体
- ✅ **无纯色信息**（配合图标或文字）
- ✅ 对比度：正文 >= 4.5:1，正常文本 >= 3:1

## 无障碍

- 图标按钮添加 `accessibilityLabel()`
- 尊重 Reduce Motion（`@Environment(\.accessibilityReduceMotion)`）
- 逻辑阅读顺序（`accessibilitySortPriority()`）
- 支持 Bold Text、增加对比度偏好

## 导航

- **Tab bar（3-5项）** 在导航期间保持可见
- **返回手势** 工作正常（永远不覆盖系统手势）
- **状态跨 Tab 保持**（`@SceneStorage`，`@State`）
- **永远不使用汉堡菜单**

## 隐私与权限

- ✅ **在上下文中请求权限**（启动时不请求）
- ✅ **系统对话框前提供自定义说明**
- ✅ 支持 Sign in with Apple
- ✅ 尊重 ATT 拒绝

## UIKit 速查

| 用途 | 组件 |
|------|------|
| 主要区块 | `UITabBarController` |
| 钻取导航 | `UINavigationController` |
| 聚焦任务 | Sheet presentation |
| 关键选择 | `UIAlertController` |
| 列表内容 | `UICollectionView` + `DiffableDataSource` |
| 网格布局 | `UICollectionViewCompositionalLayout` |
| 搜索 | `UISearchController` |
| 分享 | `UIActivityViewController` |
| 线性布局 | `UIStackView` |
| 自定义形状 | `CAShapeLayer` + `UIBezierPath` |
| 渐变 | `CAGradientLayer` |
| 动态文本 | `UIFontMetrics` + `preferredFont` |
| 深色模式 | 语义颜色 |

## SwiftUI 速查

| 用途 | 组件 |
|------|------|
| 主要区块 | `TabView` + `tabItem` |
| 钻取导航 | `NavigationStack` + `NavigationPath` |
| 聚焦任务 | `.sheet` + `presentationDetents` |
| 关键选择 | `.alert` |
| 列表内容 | `List` + `.insetGrouped` |
| 搜索 | `.searchable` |
| 分享 | `ShareLink` |
| 反馈 | `UIImpactFeedbackGenerator` |
| 动态文本 | `.font(.body)` 语义样式 |
| 深色模式 | `.primary`、`.secondary`、`Color(.systemBackground)` |
| 减少动画 | `@Environment(\.accessibilityReduceMotion)` |
| 动态字体大小 | `@Environment(\.dynamicTypeSize)` |

## 检查清单

### 布局
- [ ] 触控目标 >= 44pt
- [ ] 内容在安全区域内
- [ ] 主要操作在拇指区域
- [ ] 所有屏幕尺寸灵活宽度
- [ ] 间距对齐 8pt 网格

### 色彩
- [ ] 语义系统颜色或 light/dark Asset 变体
- [ ] 深色模式是刻意的（不只是反转）
- [ ] 无纯色信息
- [ ] 文字对比度 >= 4.5:1

### 无障碍
- [ ] 所有交互元素的 VoiceOver 标签
- [ ] 逻辑阅读顺序
- [ ] 尊重 Reduce Motion
- [ ] 所有手势有替代访问路径

### 导航
- [ ] Tab bar 用于 3-5 个顶级区块
- [ ] 无汉堡/抽屉菜单
- [ ] 返回手势全程有效
- [ ] 状态跨 Tab 保持

### 隐私
- [ ] 权限在上下文中请求（启动时不请求）
- [ ] 系统权限对话框前有自定义说明
- [ ] 提供 Sign in with Apple

## 参考文档

- `references/layout-system.md` — 触控目标、安全区域、CollectionView
- `references/navigation-patterns.md` — TabBar、NavigationController、Modal
- `references/uikit-components.md` — StackView、Button、Alert、Search、ContextMenu
- `references/graphics-animation.md` — CAShapeLayer、CAGradientLayer、Core Animation
- `references/accessibility.md` — Dynamic Type、语义颜色、VoiceOver
- `references/system-integration.md` — 权限、位置、分享、生命周期、触觉反馈
- `references/swiftui-design-guidelines.md` — SwiftUI HIG、组件、模式、反模式
- `references/swift-coding-standards.md` — Optionals、Protocols、async/await、ARC、错误处理
