# Tools 与 Systems

## Tools

`tools/` 是用户直接使用的小工具层。

主要职责：

1. 创建 PySide UI；
2. 读取用户 Selection / 输入参数；
3. 做交互级错误提示；
4. 调用 Core / System；
5. 提供统一 `main()` 入口。

推荐数据流：

```text
User
  ↓
Tool UI
  ↓
Core / System
  ↓
Maya Scene
```

Tool 不应该复制 Core 算法。

## Systems

`systems/` 用于完整、可复用的 Rig Builder / Workflow。

例如：

```text
systems/controller/
systems/face/
systems/body/skirt/
```

System 可以组合多个 Core API：

```text
curve_utils
matrix_utils
constraint_utils
connection_utils
    ↓
Face / Controller / Body Builder
```

## 如何判断放哪里

如果一个函数只是：

> “给我两个节点，我创建一条 Parent Constraint”

放 `core/constraint_utils.py`。

如果一个流程是：

> “创建控制器层级、属性、约束、Space Blend，并组织完整 Rig”

放 `systems/controller/`。

如果功能需要按钮和对象选择器：

放 `tools/`，但实际 Rig 算法仍然下沉 Core / System。
