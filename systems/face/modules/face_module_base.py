# coding=utf-8
u"""
Face Module Base
================

所有正式 Face Rig Module 共用的统一构建生命周期。

Face Workflow Step 与 Face Rig Module 是两种不同职责：

    FaceSetup / FaceGuide
        -> 使用 ModuleBase.run_step() 管理工作流 Step。

    JawModule / BrowModule / EyeModule / TeethModule / ...
        -> 使用 FaceModuleBase.build() 构建独立绑定模块。

所有 Face Rig Module 统一遵循：

    setup()
        ↓
    guide()
        ↓
    joint()
        ↓
    control()
        ↓
    connect()
        ↓
    deform()
        ↓
    finalize()

设计原则：
    1. FaceModuleBase 只规定执行顺序，不实现具体部位绑定算法；
    2. Face 公共 Config / Hierarchy / Naming 继续复用 FaceBase；
    3. Joint / Controller / Matrix / Attribute 等底层能力继续复用 Core；
    4. 具体模块只实现自己的业务阶段，不重新创建第二套通用 Helper；
    5. Scene Rebuild / Existing Node 检查由具体模块在 setup() 中处理；
    6. deform() 表示模块独有的高级绑定效果，不局限于 Maya Deformer Node。
"""

from __future__ import print_function

from ....core import scene_utils
from ..face_base import FaceBase


class FaceModuleBase(FaceBase):
    u"""所有正式 Face Rig Module 共用的七阶段模板基类。"""

    def __init__(
            self,
            side="md",
            part=None,
            index=1
    ):
        u"""
        初始化 Face Module Identity 与标准构建结果字典。

        Args:
            side (str):
                模块方向，例如 lf、rt、md。
            part (str):
                Face 模块部位，例如 jaw、brow、eye、lip、teeth。
            index (int):
                当前模块标准序号。
        """
        super(FaceModuleBase, self).__init__(
            side=side,
            part=part,
            index=index
        )

        self.module_dict = {
            "module": self,
        }

    # =========================================================================
    # Public Build Entry
    # =========================================================================

    @scene_utils.undo_chunk
    def build(self):
        u"""
        按统一七阶段生命周期完整构建 Face Module。

        Returns:
            dict:
                当前模块公开构建结果。具体节点由子类在各阶段写入 module_dict。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备模块参数、公共层级、确定性名称与 Rebuild Scene State
        # -------------------------------------------------------------------------
        self.setup()

        # -------------------------------------------------------------------------
        # Step 02：读取当前 Face Guide，并整理后续 Joint / Controller 定位数据
        # -------------------------------------------------------------------------
        self.guide()

        # -------------------------------------------------------------------------
        # Step 03：根据 Guide 创建当前模块需要的 Bind / Driver Joint
        # -------------------------------------------------------------------------
        self.joint()

        # -------------------------------------------------------------------------
        # Step 04：创建 Animator Controller，并保存完整 Controller Dict
        # -------------------------------------------------------------------------
        self.control()

        # -------------------------------------------------------------------------
        # Step 05：建立 Controller、Output、Joint 与模块内部基础驱动关系
        # -------------------------------------------------------------------------
        self.connect()

        # -------------------------------------------------------------------------
        # Step 06：创建当前模块独有的高级效果、Deformer 或辅助 Driver Network
        # -------------------------------------------------------------------------
        self.deform()

        # -------------------------------------------------------------------------
        # Step 07：验证最终 Scene State，并整理模块公开输出
        # -------------------------------------------------------------------------
        self.finalize()

        return self.module_dict

    # =========================================================================
    # ModuleBase Adapter
    # =========================================================================

    def collect_inputs(self):
        u"""把旧 ModuleBase 输入阶段映射到 Face Module setup()。"""
        return self.setup()

    def prepare_data(self):
        u"""把旧 ModuleBase 准备阶段映射到 Face Module guide()。"""
        return self.guide()

    def process_data(self):
        u"""按 Face Module 标准顺序执行 Joint、Control、Connect、Deform。"""
        # -------------------------------------------------------------------------
        # Step 01：创建 Joint
        # -------------------------------------------------------------------------
        self.joint()

        # -------------------------------------------------------------------------
        # Step 02：创建 Controller
        # -------------------------------------------------------------------------
        self.control()

        # -------------------------------------------------------------------------
        # Step 03：建立基础驱动连接
        # -------------------------------------------------------------------------
        self.connect()

        # -------------------------------------------------------------------------
        # Step 04：创建模块独有高级效果
        # -------------------------------------------------------------------------
        self.deform()

        return True

    def finalize_step(self):
        u"""把旧 ModuleBase 完成阶段映射到 Face Module finalize()。"""
        return self.finalize()

    # =========================================================================
    # Standard Face Module Lifecycle
    # =========================================================================

    def setup(self):
        u"""准备模块参数、名称、公共层级与 Rebuild Scene State。"""
        raise NotImplementedError(
            u"Face Module 子类必须实现 setup()。"
        )

    def guide(self):
        u"""读取并整理当前模块需要的 Guide 定位数据。"""
        raise NotImplementedError(
            u"Face Module 子类必须实现 guide()。"
        )

    def joint(self):
        u"""根据 Guide 创建当前模块 Joint。"""
        raise NotImplementedError(
            u"Face Module 子类必须实现 joint()。"
        )

    def control(self):
        u"""创建当前模块 Animator Controller。"""
        raise NotImplementedError(
            u"Face Module 子类必须实现 control()。"
        )

    def connect(self):
        u"""建立 Controller / Output 到 Joint 的基础驱动关系。"""
        raise NotImplementedError(
            u"Face Module 子类必须实现 connect()。"
        )

    def deform(self):
        u"""创建当前模块独有的高级绑定效果；没有特殊效果时允许保持为空。"""
        return True

    def finalize(self):
        u"""验证最终 Scene State，并整理当前 Module 的公开结果。"""
        raise NotImplementedError(
            u"Face Module 子类必须实现 finalize()。"
        )


__all__ = [
    "FaceModuleBase",
]
