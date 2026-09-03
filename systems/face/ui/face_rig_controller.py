# coding=utf-8
u"""
Face Rig Final UI Controller
============================

Face Rig UI 的最终组合入口。

当前职责：
    1. 继承 Step 04 Finalize UI Controller；
    2. 让整个 UI Workflow 统一使用 guide 包公开的正式 FaceGuide；
    3. 避免基础 face_rig_ui.py 中历史 Direct Import 固定到旧 FaceGuide Class。

这样 Step 01 -> Step 02 自动加载 Guide 时，也会使用 Long Path / Namespace
安全的 Template Root 识别逻辑，而不需要把 UI 业务复制到本文件。
"""

from __future__ import print_function

from ..guide import FaceGuide
from . import finalize_controller


class FaceRigWizard(finalize_controller.FaceRigWizard):
    u"""使用正式 FaceGuide 的最终 Face Rig Wizard。"""

    def get_face_guide(
            self,
            refresh=False
    ):
        u"""
        返回当前 UI 使用的正式 FaceGuide 实例。

        Args:
            refresh (bool):
                True 时丢弃旧实例，并重新从当前 Maya Scene 创建 FaceGuide。

        Returns:
            FaceGuide:
                当前 UI Workflow 共用的 FaceGuide。
        """
        if refresh:
            self.face_guide = None

        if self.face_guide is None:
            self.face_guide = FaceGuide()

        return self.face_guide


def main():
    u"""
    创建包含 Setup / Guide / Build / Finalize 的正式 Face Rig UI。

    Returns:
        FaceRigWizard:
            创建完成的最终 Face Rig Wizard。
    """
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
