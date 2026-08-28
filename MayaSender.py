# coding=utf-8

import socket

print(1)
class MayaSender(object):

    def __init__(self, host="127.0.0.1", port=7001):

        self.host = host
        self.port = port

    def send(self, command):
        """
        将 Python 代码发送到 Maya 执行。
        """

        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            client.connect(
                (
                    self.host,
                    self.port
                )
            )

            command_data = command.encode("utf-8")

            client.sendall(
                command_data
            )

        finally:

            client.close()


if __name__ == "__main__":

    maya = MayaSender()

    maya.send(
        """
import maya.cmds as cmds

cmds.polyCube(
    name="test_cube"
)

print("PyCharm 已成功连接 Maya")
"""
    )
