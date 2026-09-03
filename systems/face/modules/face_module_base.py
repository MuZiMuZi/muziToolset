# coding=utf-8
u"""
Face Module Base
================

所有正式 Face Rig Module 共用的统一构建生命周期。

Face Workflow Step 与 Face Rig Module 是两种不同职责：

    FaceSetup / FaceGuide
        -> 负责 Setup / Guide 工作流。

    JawModule / BrowModule / EyeModule / TeethModule / ...
        -> 使用 FaceModuleBase.create_build() 构建独立绑定模块。

所有正式 Face Rig Module 统一遵循：

    load_setup()
        ↓
    load_guide()
        ↓
    create_jnt()
        ↓
    create_ctrl()
        ↓
    create_connect()
        ↓
    create_deform()
        ↓
    create_finalize()

统一公开构建入口：

    create_build()

命名规范：
    - Class 使用 PascalCase；
    - 方法、函数、成员变量使用 snake_case；
    - Joint 在模块生命周期 API 中统一缩写为 jnt；
    - Controller 在模块生命周期 API 中统一缩写为 ctrl；
    - 常量使用 UPPER_SNAKE_CASE。

设计原则：
    1. FaceModuleBase 只规定执行顺序，不实现具体部位绑定算法；
    2. Face 公共 Config / Hierarchy / Naming 继续复用 FaceBase；
    3. Joint / Controller / Matrix / Attribute 等底层能力继续复用 Core；
    4. 具体模块只实现自己的业务阶段，不重新创建第二套通用 Helper；
    5. Scene Rebuild / Existing Node 检查由具体模块在 load_setup() 中处理；
    6. create_deform() 表示模块独有的高级绑定效果，不局限于 Maya Deformer Node；
    7. 不维护旧 Face Module Lifecycle Adapter，新模块只认本文件定义的正式 API。
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
    def create_build(self):
        u"""
        按统一七阶段生命周期完整构建 Face Module。

        Returns:
            dict:
            当前模块公开构建结果。具体节点由子类在各阶段写入 module_dict。
        """
        # -------------------------------------------------------------------------
        # Step 01：加载模块参数、公共层级、确定性名称与 Rebuild Scene State
        # -------------------------------------------------------------------------
        self.load_setup()

        # -------------------------------------------------------------------------
        # Step 02：读取当前 Face Guide，并整理后续 Joint / Controller 定位数据
        # -------------------------------------------------------------------------
        self.load_guide()

        # -------------------------------------------------------------------------
        # Step 03：根据 Guide 创建当前模块需要的 Bind / Driver Joint
        # -------------------------------------------------------------------------
        self.create_jnt()

        # -------------------------------------------------------------------------
        # Step 04：创建 Animator Controller，并保存完整 Controller Dict
        # -------------------------------------------------------------------------
        self.create_ctrl()

        # -------------------------------------------------------------------------
        # Step 05：建立 Controller、Output、Joint 与模块内部基础驱动关系
        # -------------------------------------------------------------------------
        self.create_connect()

        # -------------------------------------------------------------------------
        # Step 06：创建当前模块独有的高级效果、Deformer 或辅助 Driver Network
        # -------------------------------------------------------------------------
        self.create_deform()

        # -------------------------------------------------------------------------
        # Step 07：验证最终 Scene State，并整理模块公开输出
        # -------------------------------------------------------------------------
        self.create_finalize()

        return self.module_dict

    # =========================================================================
    # Standard Face Module Lifecycle
    # =========================================================================

    def load_setup(self):
        u"""
        加载模块参数、名称、公共层级与 Rebuild Scene State。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"Face Module 子类必须实现 load_setup()。"
        )

    def load_guide(self):
        u"""
        读取并整理当前模块需要的 Guide 定位数据。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"Face Module 子类必须实现 load_guide()。"
        )

    def create_jnt(self):
        u"""
        根据 Guide 创建当前模块 Joint。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"Face Module 子类必须实现 create_jnt()。"
        )

    def create_ctrl(self):
        u"""
        创建当前模块 Animator Controller。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"Face Module 子类必须实现 create_ctrl()。"
        )

    def create_connect(self):
        u"""
        建立 Controller / Output 到 Joint 的基础驱动关系。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"Face Module 子类必须实现 create_connect()。"
        )

    def create_deform(self):
        u"""

                创建当前模块独有的高级绑定效果；没有特殊效果时允许保持为空。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        return True

    def create_finalize(self):
        u"""
        验证最终 Scene State，并整理当前 Module 的公开结果。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"Face Module 子类必须实现 create_finalize()。"
        )


__all__ = [
    "FaceModuleBase",
]
