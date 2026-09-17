# coding=utf-8
u"""
EyePairModule：双眼系统总模块。

这个模块不重新实现单只眼睛的 Joint / Controller / Aim 算法。
左眼和右眼仍然分别交给 EyeModule 负责，EyePairModule 只负责把两只眼睛
组合成一个完整的双眼系统，并增加一个中间 Aim 总控制器。

创建流程：
    build_rig()
        -> 创建左眼 EyeModule
        -> 创建右眼 EyeModule
        -> 在左右 Aim Guide 中间创建 ctrl_md_eye_aim_001

连接流程：
    connect_rig()
        -> 左眼建立自己的 Aim / Orient Constraint
        -> 右眼建立自己的 Aim / Orient Constraint
        -> 中间 Aim Output 通过 Point Constraint 驱动左右 Aim Driven

最终控制关系：

    ctrl_md_eye_aim_001
        |
        +--> driven_lf_eye_aim_001
        |       -> ctrl_lf_eye_aim_001
        |       -> 左眼 Aim
        |
        +--> driven_rt_eye_aim_001
                -> ctrl_rt_eye_aim_001
                -> 右眼 Aim

这样：
    1. 移动中间 Aim，可以同时控制两只眼睛的观察目标。
    2. 左右 Aim Controller 仍然可以分别做单眼偏移。
    3. 不需要改变 EyeModule 已经稳定的内部结构。
"""

import maya.cmds as cmds

from ...core.common import name_utils, hierarchy_utils
from ...core.rigging import ctrl_utils
from .eye_module import EyeModule


class EyePairModule(object):
    u"""统一管理左右 EyeModule 和中间 Eye Aim 总控制器。"""

    def __init__(
        self,
        lf_guide=None,
        rt_guide=None,
        jnt_parent=None,
        ctrl_parent=None,
        master_aim_ctrl_shape="circle",
        master_aim_ctrl_color=17,
        master_aim_ctrl_size=18.0,
        master_aim_ctrl_axis="Z+"
    ):
        u"""
        初始化双眼模块、稳定节点名称和中间 Aim Controller 设置。

        Args:
            lf_guide (str):
                当前 Rig 定位流程使用的 Guide / Locator Transform。
            rt_guide (str):
                当前 Rig 定位流程使用的 Guide / Locator Transform。
            jnt_parent (str | None):
                新建 Jnt Chain 的父 Jnt / Parent Transform；None 表示保持在世界层级。
            ctrl_parent (object):
                当前方法执行 Maya / Rig 操作时使用的 `ctrl_parent` 数据。
            master_aim_ctrl_shape (str):
                当前 Maya / Rig 操作使用的 `master_aim_ctrl_shape` 名称或标记。
            master_aim_ctrl_color (int):
                当前 Maya / Rig 操作使用的 `master_aim_ctrl_color` 整数参数。
            master_aim_ctrl_size (float):
                当前 Maya / Rig 计算使用的 `master_aim_ctrl_size` 数值参数。
            master_aim_ctrl_axis (str):
                当前 Maya / Rig 操作使用的 `master_aim_ctrl_axis` 名称或标记。
        """

        # FaceModule 会把左右两套 Eye Guide 分别传进来。
        self.lf_guide = lf_guide
        self.rt_guide = rt_guide
        self.jnt_parent = jnt_parent
        self.ctrl_parent = ctrl_parent

        # 中间 Aim 总控制器只负责同时移动左右两个 Aim Target。
        self.master_aim_ctrl_shape = master_aim_ctrl_shape
        self.master_aim_ctrl_color = master_aim_ctrl_color
        self.master_aim_ctrl_size = master_aim_ctrl_size
        self.master_aim_ctrl_axis = master_aim_ctrl_axis

        # 左右 EyeModule 仍然各自负责自己的 Joint、Controller 和 Constraint。
        self.lf_eye = EyeModule(
            side="lf",
            guide=self.lf_guide,
            jnt_parent=self.jnt_parent,
            ctrl_parent=self.ctrl_parent
        )

        self.rt_eye = EyeModule(
            side="rt",
            guide=self.rt_guide,
            jnt_parent=self.jnt_parent,
            ctrl_parent=self.ctrl_parent
        )

        # 中间 Aim Controller 使用 md 方向。
        # 它不是第三只眼睛，只是左右 Aim Controller 的总控。
        self.master_aim_ctrl_name = name_utils.Name(type="ctrl", side="md", part="eye", function="aim", index=1).name
        self.master_aim_zero_name = self.master_aim_ctrl_name.replace("ctrl_", "zero_", 1)
        self.master_aim_output_name = self.master_aim_ctrl_name.replace("ctrl_", "output_", 1)

        # 左右 Aim Driven 也是稳定节点名称。
        # EyePairModule 需要直接把中间 Aim 的位移结果送到这两个 Driven Group，
        # 所以初始化时就确定名称，连接阶段不再通过场景反查。
        self.lf_aim_driven_name = self.lf_eye.aim_ctrl_name.replace("ctrl_", "driven_", 1)
        self.rt_aim_driven_name = self.rt_eye.aim_ctrl_name.replace("ctrl_", "driven_", 1)

        # 中间 Aim 只驱动左右 Aim Controller 的 Driven Group。
        # Point Constraint 只传递位置，避免总控旋转对左右 Aim 产生不需要的旋转影响。
        self.lf_aim_point_constraint_name = name_utils.Name(type="pointConstraint", side="lf", part="eye", function="aim", index=1).name
        self.rt_aim_point_constraint_name = name_utils.Name(type="pointConstraint", side="rt", part="eye", function="aim", index=1).name

        # build_rig() 创建以后保存 Ctrl 工具对象。
        # 稳定 Maya 节点身份仍然以上面的名称变量为准。
        self.master_aim_ctrl_object = None

    def get_master_aim_position(self):
        u"""

                计算左右 Aim Guide 的中间位置。

                Locator Transform 本身就是 Guide 定位数据，因此这里直接读取左右 Aim Locator
                的世界空间 Transform，不读取 Locator Shape 的 localPosition / worldPosition。

                Returns:
                    tuple:
                        按当前 API 约定组织的结果元组。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                
        """

        if not self.lf_guide or len(self.lf_guide) != 3:
            raise RuntimeError(u"左眼需要 Ball / Iris / Aim 三个 Guide。")

        if not self.rt_guide or len(self.rt_guide) != 3:
            raise RuntimeError(u"右眼需要 Ball / Iris / Aim 三个 Guide。")

        lf_aim_guide = self.lf_guide[2]
        rt_aim_guide = self.rt_guide[2]

        if not cmds.objExists(lf_aim_guide):
            raise RuntimeError(u"找不到左眼 Aim Guide：{}".format(lf_aim_guide))

        if not cmds.objExists(rt_aim_guide):
            raise RuntimeError(u"找不到右眼 Aim Guide：{}".format(rt_aim_guide))

        lf_position = cmds.xform(
            lf_aim_guide,
            query=True,
            worldSpace=True,
            translation=True
        )

        rt_position = cmds.xform(
            rt_aim_guide,
            query=True,
            worldSpace=True,
            translation=True
        )

        middle_x = (lf_position[0] + rt_position[0]) * 0.5
        middle_y = (lf_position[1] + rt_position[1]) * 0.5
        middle_z = (lf_position[2] + rt_position[2]) * 0.5

        return middle_x, middle_y, middle_z

    def create_master_aim_ctrl(self):
        u"""

                在左右 Aim Guide 中间创建双眼 Aim 总控制器。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。
                
        """

        self.master_aim_ctrl_object = ctrl_utils.Ctrl(self.master_aim_ctrl_name)

        self.master_aim_ctrl_object.create_ctrl(
            shape_name=self.master_aim_ctrl_shape,
            ctrl_color=self.master_aim_ctrl_color,
            ctrl_size=self.master_aim_ctrl_size,
            ctrl_axis=self.master_aim_ctrl_axis,
            create_hierarchy=True
        )

        # Controller 完整层级已经创建以后，只移动 Zero Group。
        # 这样 ctrl_md_eye_aim_001 自身仍然保持干净的 Translate / Rotate / Scale。
        master_position = self.get_master_aim_position()

        cmds.xform(
            str(self.master_aim_ctrl_object.zero_grp),
            worldSpace=True,
            translation=master_position
        )

        # 中间 Aim 属于整个 Face Controller 系统，直接把 Zero Group 放到 Face Ctrl 总组。
        if self.ctrl_parent:
            hierarchy_utils.parent(
                self.master_aim_ctrl_object.zero_grp,
                self.ctrl_parent
            )

        return self.master_aim_ctrl_name

    def build_rig(self):
        u"""

                创建完整双眼系统，但暂时不建立 Constraint。

                顺序：
                    1. 创建左眼。
                    2. 创建右眼。
                    3. 创建中间 Aim 总控制器。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。
                
        """

        self.lf_eye.build_rig()
        self.rt_eye.build_rig()
        self.create_master_aim_ctrl()

        return {
            "lf_eye": self.lf_eye,
            "rt_eye": self.rt_eye,
            "master_aim": self.master_aim_ctrl_name,
        }

    def connect_rig(self):
        u"""

                建立左右眼自己的连接，并让中间 Aim 总控驱动左右 Aim Driven Group。

                Point Constraint 使用 maintainOffset=True。
                创建连接时左右 Aim Controller 不会跳到中间位置，而是保留当前左右间距；
                后续移动中间 Aim Controller 时，两边 Aim Target 会一起移动相同距离。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                
        """

        lf_result = self.lf_eye.connect_rig()
        rt_result = self.rt_eye.connect_rig()

        required_nodes = [
            self.master_aim_output_name,
            self.lf_aim_driven_name,
            self.rt_aim_driven_name,
        ]

        for node_name in required_nodes:
            if not cmds.objExists(node_name):
                raise RuntimeError(u"Eye Pair Rig 节点不存在：{}".format(node_name))

        if not cmds.objExists(self.lf_aim_point_constraint_name):
            cmds.pointConstraint(
                self.master_aim_output_name,
                self.lf_aim_driven_name,
                maintainOffset=True,
                name=self.lf_aim_point_constraint_name
            )

        if not cmds.objExists(self.rt_aim_point_constraint_name):
            cmds.pointConstraint(
                self.master_aim_output_name,
                self.rt_aim_driven_name,
                maintainOffset=True,
                name=self.rt_aim_point_constraint_name
            )

        return {
            "lf_eye": lf_result,
            "rt_eye": rt_result,
            "lf_master_aim": self.lf_aim_point_constraint_name,
            "rt_master_aim": self.rt_aim_point_constraint_name,
        }

    def delete_rig(self):
        u"""

                删除双眼连接、左右 EyeModule 和中间 Aim 总控制器。

                Returns:
                    list:
                        按当前 API 约定顺序返回的结果列表。
                
        """

        # 先删除总控到左右 Aim Driven 的两个 Point Constraint。
        if cmds.objExists(self.lf_aim_point_constraint_name):
            cmds.delete(self.lf_aim_point_constraint_name)

        if cmds.objExists(self.rt_aim_point_constraint_name):
            cmds.delete(self.rt_aim_point_constraint_name)

        # 左右 EyeModule 继续负责删除各自拥有的节点。
        self.lf_eye.delete_rig()
        self.rt_eye.delete_rig()

        # 中间 Aim Controller 从 Zero Group 开始删除整个标准 Controller Hierarchy。
        if cmds.objExists(self.master_aim_zero_name):
            cmds.delete(self.master_aim_zero_name)

        self.master_aim_ctrl_object = None

        return [
            self.master_aim_zero_name,
            self.lf_eye.jnt_master_grp,
            self.lf_eye.ctrl_master_grp,
            self.rt_eye.jnt_master_grp,
            self.rt_eye.ctrl_master_grp,
        ]
