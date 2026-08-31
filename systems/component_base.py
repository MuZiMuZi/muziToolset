# coding=utf-8
u"""
Rig Component Base
==================

所有 Rig Component 共用的核心构建规范。

适用范围
--------
只要一个 Rig 模块需要经过多阶段构建，例如：
    - Single Control Rig；
    - FK Rig；
    - IK Rig；
    - IK / FK Rig；
    - Face Rig Component；
    - Jaw / Teeth / Tongue / Eye / Brow；
    - Spine / Ribbon 等其它 Rig Component；
都可以继承本类，并统一按照以下顺序组织核心构建代码：

    create_joint()
    create_controller()
    create_connection()

设计目的
--------
1. 让所有 Rig Component 的 process_data() 保持一致；
2. 把 Joint、Controller、Connection 三类职责明确分开；
3. 当具体 Rig 越来越复杂时，可以继续在三大阶段内部拆分小方法；
4. 本类只定义 Rig 构建规范，不依赖 Face / Body 等具体业务；
5. Maya Joint、Controller、Constraint、Matrix 等实际实现继续由 core / systems 专项模块负责。
"""

from __future__ import print_function


class ComponentBase(object):
    u"""所有多阶段 Rig Component 共用的构建规范。"""

    def process_data(self):
        u"""
        按照统一顺序执行 Rig Component 的核心构建。

        Returns:
            bool:
            三个核心构建阶段全部执行完成后返回 True。
        """
        # 创建当前 Rig Component 所需的 Joint 或 Joint Chain。
        self.create_joint()

        # 创建当前 Rig Component 所需的 Controller 和 Controller Hierarchy。
        self.create_controller()

        # 建立 Controller、Joint、Deformer 和其它 Rig Node 之间的驱动关系。
        self.create_connection()

        return True

    def create_joint(self):
        u"""
        创建当前 Rig Component 所需的 Joint。

        具体实现由子类负责，例如：
            - 单 Joint；
            - FK Joint Chain；
            - IK Joint Chain；
            - Bind Joint Chain；
            - Face Component Joint。
        """
        raise NotImplementedError(
            u"子类必须实现 create_joint()。"
        )

    def create_controller(self):
        u"""
        创建当前 Rig Component 所需的 Controller。

        具体实现由子类负责，例如：
            - 单控制器；
            - FK Controller Chain；
            - IK Controller；
            - Pole Vector Controller；
            - Face Component Controller。
        """
        raise NotImplementedError(
            u"子类必须实现 create_controller()。"
        )

    def create_connection(self):
        u"""
        建立当前 Rig Component 的最终驱动关系。

        具体实现由子类负责，例如：
            - Controller -> Joint；
            - FK Chain -> Bind Chain；
            - IK Handle / Pole Vector；
            - Matrix / Constraint；
            - Deformer / Rig Node Connection。
        """
        raise NotImplementedError(
            u"子类必须实现 create_connection()。"
        )


__all__ = [
    "ComponentBase",
]
