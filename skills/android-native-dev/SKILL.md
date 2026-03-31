---
name: android-native-dev
description: |
  Android 原生应用开发指南，涵盖 Material Design 3、Kotlin/Jetpack Compose 开发、
  项目配置、无障碍访问和构建故障排除。
  触发条件：开发 Android 原生应用、实现 UI、使用 Kotlin/Compose 布局、
  构建 Android 应用、Material Design 合规检查。
license: MIT
metadata:
  category: mobile
  version: 1.0.0
sources:
  - Material Design 3 Guidelines (material.io)
  - Android Developer Documentation (developer.android.com)
  - Google Play Quality Guidelines
  - WCAG Accessibility Guidelines
---

# Android 原生开发规范

## 项目初始化前置检查

| 场景 | 特征 | 方法 |
|------|------|------|
| **空目录** | 无文件 | 完整初始化，包含 Gradle Wrapper |
| **有 Gradle Wrapper** | gradlew 和 gradle/wrapper/ 存在 | 直接用 ./gradlew 构建 |
| **Android Studio 项目** | 完整项目结构 | 检查 wrapper，按需运行 gradle wrapper |
| **不完整项目** | 部分文件存在 | 检查缺失文件，完成配置 |

**关键原则**：写业务逻辑前，确保 `./gradlew assembleDebug` 成功。

## Gradle 配置

### gradle.properties（必须）
```properties
android.useAndroidX=true
android.enableJetifier=true
org.gradle.parallel=true
kotlin.code.style=official
# 大型项目：org.gradle.jvmargs=-Xmx8192m
```

### 依赖声明规范
```kotlin
dependencies {
  // 用 BOM 管理 Compose 版本
  implementation(platform("androidx.compose:compose-bom:2024.02.00"))
  implementation("androidx.compose.ui:ui")
  implementation("androidx.compose.material3:material3")
  implementation("androidx.activity:activity-compose:1.8.2")
  implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
}
```

### Product Flavors 配置
```kotlin
android {
  flavorDimensions += "environment"
  productFlavors {
    create("dev") {
      dimension = "environment"
      applicationIdSuffix = ".dev"
      versionNameSuffix = "-dev"
      buildConfigField("String", "API_BASE_URL", "\"https://dev-api.example.com\"")
      buildConfigField("Boolean", "ENABLE_LOGGING", "true")
    }
    create("prod") {
      dimension = "environment"
      // 生产无后缀
      buildConfigField("String", "API_BASE_URL", "\"https://api.example.com\"")
      buildConfigField("Boolean", "ENABLE_LOGGING", "false")
    }
  }
}
```

## Kotlin 开发标准

### 线程与协程（关键）
| 操作类型 | 线程 | 用途 |
|---------|------|------|
| UI 更新 | `Dispatchers.Main` | 更新 View、State、LiveData |
| 网络请求 | `Dispatchers.IO` | HTTP 调用、API 请求 |
| 文件 I/O | `Dispatchers.IO` | 本地存储、数据库操作 |
| 计算密集 | `Dispatchers.Default` | JSON 解析、排序、加密 |

**常见错误：**
```kotlin
// ❌ 错误：在 IO 线程更新 UI
viewModelScope.launch(Dispatchers.IO) {
  val data = api.fetch()
  _uiState.value = data // 崩溃！
}
// ✅ 正确：IO 获取，Main 更新
viewModelScope.launch {
  val data = withContext(Dispatchers.IO) { api.fetch() }
  _uiState.value = data
}
```

### 空安全
```kotlin
// ❌ 避免：非空断言 !!（可能崩溃）
val name = user!!.name
// ✅ 推荐：安全调用 + 默认值
val name = user?.name ?: "Unknown"
```

### 服务器响应 DTO 必须可空
```kotlin
// ❌ 错误：字段声明为非空
data class UserResponse(
  val id: String = "",
  val name: String = "",
)
// ✅ 正确：所有字段可空
data class UserResponse(
  @SerializedName("id") val id: String? = null,
  @SerializedName("name") val name: String? = null,
)
```

## Jetpack Compose 规范

### @Composable 上下文规则
```kotlin
// ❌ 错误：从非 Composable 调用 Composable
fun showError(message: String) {
  Text(message) // 编译错误！
}
// ✅ 正确：标记为 @Composable
@Composable
fun ErrorMessage(message: String) {
  Text(message)
}
```

### 状态管理
```kotlin
// 基础 State
var count by remember { mutableStateOf(0) }
// 派生 State（避免冗余计算）
val isEven by remember { derivedStateOf { count % 2 == 0 } }
// ViewModel 中的 State
val uiState: StateFlow by _uiState.asStateFlow()
```

## Material Design 3 核心原则

| 原则 | 描述 |
|------|------|
| **Personal** | 基于用户偏好的动态配色 |
| **Adaptive** | 响应所有屏幕尺寸和形态 |
| **Expressive** | 充满情感的 UX，鲜艳生动配色 |
| **Accessible** | 包容性设计 |

### 触控目标
| 类型 | 尺寸 |
|------|------|
| 最小 | 48 × 48dp |
| 推荐（主要操作） | 56 × 56dp |
| 儿童应用 | 56dp+ |

### 8dp 网格系统
| Token | 值 | 用途 |
|-------|---|------|
| xs | 4dp | 图标内边距 |
| sm | 8dp | 紧凑间距 |
| md | 16dp | 默认内边距 |
| lg | 24dp | 区块间距 |
| xl | 32dp | 大间距 |

### 动画时长
| 类型 | 时长 |
|------|------|
| 微交互（涟漪） | 50-100ms |
| 简单 | 100-200ms |
| 展开/折叠 | 200-300ms |
| 复杂 | 300-500ms |

## 无障碍设计

- ✅ 所有交互元素添加 `contentDescription`
- ✅ 尊重 Bold Text、Increase Contrast 偏好
- ✅ 复杂手势提供替代访问路径
- ✅ 色彩对比度：正文 4.5:1+，大文本 3:1+

## 构建错误诊断

| 错误关键词 | 原因 | 修复 |
|-----------|------|------|
| `Unresolved reference` | 缺少导入或未定义 | 检查导入，验证依赖 |
| `Type mismatch` | 类型不兼容 | 检查参数类型，添加转换 |
| `Cannot access` | 可见性问题 | 检查 public/private/internal |
| `@Composable invocations` | Composable 上下文错误 | 确保调用者也是 @Composable |
| `Duplicate class` | 依赖冲突 | 用 `./gradlew dependencies` 排查 |

## 反模式（禁止）

- 底部导航超过 5 项
- 多个 FAB 在同一屏幕
- 触控目标小于 48dp
- 缺少深色主题支持
- 启动时间超过 2 秒无进度指示
- 纯色信息（无图标或文字配合）

## 详细参考

- `references/visual-design.md` — 配色、排版、间距、形状
- `references/motion-system.md` — 动画与过渡
- `references/accessibility.md` — 无障碍设计
- `references/adaptive-screens.md` — 大屏与折叠屏
- `references/performance-stability.md` — 性能与稳定性
- `references/privacy-security.md` — 隐私与安全
- `references/functional-requirements.md` — 音视频、通知
- `references/design-style-guide.md` — 按类别应用风格
