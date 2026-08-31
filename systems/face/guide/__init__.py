# coding=utf-8
u"""Face Rig Step 02 - Guide。"""

from __future__ import print_function

from .face_guide import FaceGuide


class _GuideMirrorCompatibility(object):
    u"""旧 UI Mirror 调用的轻量兼容转发，不保存任何独立实现。"""

    @staticmethod
    def mirror_guides(
            face_guide,
            source_side,
            target_side
    ):
        return face_guide.mirror_guides(
            source_side=source_side,
            target_side=target_side
        )

    @staticmethod
    def undo_mirror(
            face_guide,
            snapshot
    ):
        return face_guide.undo_mirror(
            snapshot
        )


guide_mirror = _GuideMirrorCompatibility()


__all__ = [
    "FaceGuide",
    "guide_mirror",
]
