# coding=utf-8
u"""
主工具箱展示目录
================

职责：
    1. 保存工具显示名称、简介和分类文案；
    2. 解析 Tool Registry Runner 的运行模式；
    3. 为主工具箱 Widget 提供不依赖 Qt 的展示数据。

非职责：
    - 不创建 Qt Widget；
    - 不打开 Maya 工具窗口；
    - 不扫描 Tool Registry。
"""

from __future__ import print_function


TOOL_MODE_UI = "ui"
TOOL_MODE_ACTION = "action"


tool_display_names = {
    "rename_tool": u"重命名工具",
    "attr_tool": u"属性工具",
    "connections_tool": u"连接工具",
    "constraint_tool": u"约束工具",
    "snap_tool": u"快速吸附",
    "jnt_tool": u"Jnt 工具",
    "jnt_resamp_tool": u"关节链重采样",
    "control_shape_tool": u"控制器 Shape 图库",
    "create_ctrl_tool": u"创建控制器",
    "create_fk_ctrl_tool": u"创建 FK 控制器",
    "face_rig_tool": u"面部绑定库",
    "modular_rig_tool": u"模块化绑定库",
    "rig_tool": u"Rig 工具",
    "skirt_ctrl_tool": u"裙子绑定工具",
    "face_select_key_tool": u"面部 Driven Key",
    "skin_tool": u"Skin 工具",
    "add_blendshape_tool": u"BlendShape Target",
    "invert_shape_tool": u"Invert Shape",
    "hierarchy_cleaner": u"层级清理器",
    "model_checker": u"模型检查器",
}


tool_descriptions = {
    "rename_tool": u"批量命名、替换、前后缀与层级重命名。",
    "attr_tool": u"属性编辑、Channel Box 排序、锁定与隐藏。",
    "connections_tool": u"Transform、自定义属性与已有连接管理。",
    "constraint_tool": u"常用约束创建、查询和删除。",
    "snap_tool": u"按当前选择立即执行位置、旋转和矩阵吸附。",
    "jnt_tool": u"Jnt 创建、显示、镜像与常用骨骼操作。",
    "jnt_resamp_tool": u"在关节区间安全插入并重新分布 Jnt。",
    "control_shape_tool": u"浏览、替换、缩放、旋转与管理 Controller Shape。",
    "create_ctrl_tool": u"创建标准控制器层级、颜色、轴向与输出结构。",
    "create_fk_ctrl_tool": u"按当前选择顺序立即创建 FK Controller 链。",
    "face_rig_tool": u"Ear、Tongue、FK Chain 模块与面部起步模板。",
    "modular_rig_tool": u"模块与模板、Guide、构建及控制器外观。",
    "rig_tool": u"FK、IK、PV、层级、约束等常用绑定操作。",
    "skirt_ctrl_tool": u"裙子定位曲线、Blueprint、Bind Jnt 与 FK 创建。",
    "face_select_key_tool": u"快速建立面部 Driven Key 驱动关系。",
    "skin_tool": u"SkinCluster、复制权重、权重文件与影响骨骼管理。",
    "add_blendshape_tool": u"BlendShape Target 查询、复制与管理。",
    "invert_shape_tool": u"基于 Maya invertShape 的修型反算工具。",
    "hierarchy_cleaner": u"安全清理层级、空组与可清理历史。",
    "model_checker": u"模型拓扑、命名、Transform 与历史检查。",
}


category_descriptions = {
    u"基础工具": u"命名、属性、连接、约束、吸附等通用 Maya 操作。",
    u"骨骼工具": u"Jnt 创建、编辑、镜像与关节链处理。",
    u"控制器工具": u"Controller 创建、Shape 图库与 FK Controller。",
    u"绑定工具": u"Rig、IK / FK、PV 与专项绑定工具。",
    u"面部工具": u"Face Rig 入口与 Driven Key 面部驱动。",
    u"蒙皮工具": u"SkinCluster、权重复制与权重文件管理。",
    u"BlendShape 工具": u"BlendShape Target 与修型反算。",
    u"检查与清理": u"模型检查、层级检查与安全场景清理。",
}


category_short_names = {
    u"基础工具": "BASIC",
    u"骨骼工具": "JOINT",
    u"控制器工具": "CONTROL",
    u"绑定工具": "RIG",
    u"面部工具": "FACE",
    u"蒙皮工具": "SKIN",
    u"BlendShape 工具": "SHAPE",
    u"检查与清理": "CLEAN",
}


def get_tool_display_name(tool_name):
    u"""
    返回工具卡片显示名称。

    Args:
        tool_name (str):
            Tool Registry 中的模块短名称。

    Returns:
        str:
        中文显示名称；未登记时返回由模块名转换出的标题。
    """
    if tool_name in tool_display_names:
        return tool_display_names[tool_name]

    display_words = []

    for word in tool_name.split("_"):
        if word:
            display_words.append(word.title())

    return " ".join(display_words)


def get_tool_description(tool_name):
    u"""
    返回工具卡片的一行功能说明。

    Args:
        tool_name (str):
            Tool Registry 中的模块短名称。

    Returns:
        str:
        工具用途简介；未登记时返回通用运行说明。
    """
    if tool_name in tool_descriptions:
        return tool_descriptions[tool_name]

    return u"运行 {} 模块。".format(tool_name)


def get_tool_mode(tool_function):
    u"""
    读取 Tool Registry Runner 声明的运行模式。

    Args:
        tool_function (callable):
            Tool Registry 创建的懒加载 Runner。

    Returns:
        str:
        ``ui`` 或 ``action``；未声明时保持旧工具的 ``ui`` 行为。
    """
    tool_mode = getattr(tool_function, "tool_mode", TOOL_MODE_UI)

    if tool_mode == TOOL_MODE_ACTION:
        return TOOL_MODE_ACTION

    return TOOL_MODE_UI


def get_tool_mode_display_name(tool_mode):
    u"""
    把工具运行模式转换成中文显示名称。

    Args:
        tool_mode (str):
            ``ui`` 或 ``action`` 运行模式。

    Returns:
        str:
        ``界面工具`` 或 ``直接执行``。
    """
    if tool_mode == TOOL_MODE_ACTION:
        return u"直接执行"

    return u"界面工具"


__all__ = [
    "TOOL_MODE_ACTION",
    "TOOL_MODE_UI",
    "category_descriptions",
    "category_short_names",
    "get_tool_description",
    "get_tool_display_name",
    "get_tool_mode",
    "get_tool_mode_display_name",
]
