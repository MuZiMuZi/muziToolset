# coding=utf-8
u"""Maya Undo 上下文。"""

from __future__ import print_function

from contextlib import contextmanager

import pymel.core as pm


@contextmanager
def undo_chunk(chunk_name="muzi_toolset"):
    u"""把一段 Maya 操作包进一个 Undo Chunk。"""
    pm.undoInfo(
        openChunk=True,
        chunkName=chunk_name
    )

    try:
        yield
    finally:
        pm.undoInfo(
            closeChunk=True
        )


__all__ = [
    "undo_chunk",
]
