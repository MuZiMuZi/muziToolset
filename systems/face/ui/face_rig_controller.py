# coding=utf-8
u"""
Face Rig Final UI Controller
============================

Face Rig UI 的最终组合入口。

当前职责：
    1. 继承完整 Workflow Lifecycle Controller；
    2. 让整个 UI Workflow 统一使用 guide 包公开的正式 FaceGuide；
    3. 保持 Guide Long Path / Namespace 安全查询；
    4. 统一启用“只允许底部下一步向前、回退自动清理、Guide Snapshot 持久化”的正式流程。
"""

from __future__ import print_function

from ..guide import FaceGuide
from . import lifecycle_controller


class FaceRigWizard(lifecycle_controller.FaceRigWizard):
    u"""使用正式 FaceGuide 与 Workflow Lifecycle 的最终 Face Rig Wizard。"""

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
    创建包含 Setup / Guide / Build / Finalize 生命周期管理的正式 Face Rig UI。

    Returns:
        FaceRigWizard:
            创建完成的最终 Face Rig Wizard。
    """
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
