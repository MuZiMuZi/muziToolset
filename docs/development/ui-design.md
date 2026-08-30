# MuziTools UI Design System

MuziTools 的正式 UI 统一使用 `ui/theme.py` 和 `ui/widgets/`。

当前视觉方向参考 Arc Browser 的信息组织原则：**clean and calm、sidebar-first、减少视觉噪音、用层级而不是大量边框组织内容**。这里借鉴的是交互和布局思想，不复制 Arc 的 Logo、品牌素材、专有图标或一比一视觉资产。

## 设计目标

```text
用户当前任务
    ↓
只展示当前需要处理的内容
    ↓
次要能力收进弱层级
    ↓
危险 / 修复 / 下一步操作保持明确可见
```

正式 UI 应做到：

- 主窗口优先使用稳定 Sidebar / Content 结构；
- Workflow 工具优先使用清晰的 Step Navigation；
- Content 使用柔和背景和浮层式 Card；
- 边框低对比，但按钮和输入焦点必须清楚；
- Primary Button 只用于当前页面最主要动作；
- Secondary Button 用于 Mirror、Repair、Apply 等需要明确可见的辅助动作；
- Ghost Button 只用于低风险、低频、可忽略操作；
- Error / Warning 不能只依赖颜色，必须有清楚文本；
- Tool 不应单独复制完整 QSS，优先扩展 `ui/theme.py`；
- 可复用复合控件放在 `ui/widgets/`。

## Theme Token

默认主题使用柔和冷灰和淡紫强调：

```text
background          应用背景
sidebar_background  Sidebar 背景
surface             主内容 Surface
surface_alt         次级 Surface
border              普通边界
border_soft         弱边界
accent              主强调色
accent_soft         选中 / Hover 柔和背景
text                主文字
text_secondary      普通说明
text_muted          弱说明
```

业务代码不要直接假设具体 Hex 值。需要主题色时应读取 `ui.theme`。

## Button 层级

### Primary

适合：

- 下一步
- 创建
- Build
- Publish
- 当前窗口唯一主要提交动作

```python
from muziToolset.ui import theme

theme.style_primary(button)
```

### Secondary

适合：

- LF → RT
- RT → LF
- 重新导入模板
- Apply
- Refresh Data

```python
theme.style_secondary(button)
```

### Ghost

适合：

- 关闭次级内容
- 不影响主要流程的低频操作
- 弱化的 Utility Action

```python
theme.style_ghost(button)
```

### Danger

只用于明确破坏数据的操作，例如 Delete / Reset Result。

```python
theme.style_danger(button)
```

## Card 规则

同一页面不要通过大量 GroupBox 和粗分割线制造层级。

推荐：

```text
Page
├── Card: Current State
├── Card: Main Task
├── Card: Settings
└── Bottom Primary Action
```

使用：

```python
card, layout = theme.make_card(parent)
```

次级区域：

```python
sub_card, layout = theme.make_sub_card(parent)
```

## Sidebar / Navigation

主工具箱继续使用左侧固定分类 Sidebar。Active Item 应使用柔和 Surface，而不是高饱和色块。

Workflow Wizard 例如 Face Rig：

```text
01 Setup   02 Guide   03 Build   04 Finalize
```

当前 Step 明确，完成过的 Step 可以返回，未来 Step 在前置条件未满足时保持 Disabled。

## Input

- 单行参数优先 `QSpinBox / QDoubleSpinBox / QComboBox`；
- 连续或可视化范围适合 Slider；
- 需要准确输入的 Size 不使用纯 Slider；
- Controller Size 使用 `QDoubleSpinBox`：一位小数，步进 `0.1`；
- Controller Color 使用 `MayaIndexColorSlider`，同时显示 Slider、Index 和 Color Preview。

## Face Rig Step 02 示例

```text
Face Guide
    Guide 完整状态
    [重新导入模板]

Guide Mirror
    [LF → RT] [RT → LF] [撤销上次镜像]

Controller Settings
    Global Scale
    LF / RT / MD Color
    Brow / Eye / Eyelid / Nose / Cheek / Lip / Jaw Size

                                      [下一步]
```

Mirror / Repair 都属于明确辅助动作，因此使用 Secondary Button，而不是弱到难以发现的 Ghost Button。

## 可复用 Widget

```text
ui/widgets/
├── object_picker.py
└── color_index_slider.py
```

后续出现重复 UI 组合时，优先提取 Widget，不要在多个 Tool 中复制。

## 新 UI Review Checklist

提交新 UI 前检查：

1. 是否复用 `theme.style_window()`；
2. 是否存在重复大段 QSS；
3. Primary Button 是否只有真正的主操作；
4. 关键按钮是否因为 Ghost 样式而过弱；
5. 内容是否可以通过 Card / Section 层级理解；
6. 参数控件是否与数据类型匹配；
7. 错误信息是否明确告诉用户如何恢复；
8. PySide2 / PySide6 fallback 是否保持一致；
9. UI 是否只做 UI，不复制 System / Core 算法。
