# coding=utf-8
u"""Legacy compatibility wrapper for :mod:`MuziTools.tools.basic.connections_tool`."""

from .tools.basic.connections_tool import ConnectionsTool
from .tools.basic.connections_tool import main


Connections_Tool = ConnectionsTool


__all__ = [
    "ConnectionsTool",
    "Connections_Tool",
    "main",
]
