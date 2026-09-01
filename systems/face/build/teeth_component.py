# coding=utf-8
u"""
Teeth Component
===============

用于构建上下牙床的 Face Rig Component。

继承关系：
    ComponentBase
        -> RigComponentBase
            -> FaceBase
                -> TeethComponent

Teeth Component 使用 RigComponentBase 提供的标准 process_data()：
    1. create_joint()；
    2. create_controller()；
    3. create_connection()。

当前职责：
    - 根据 Teeth Guide 创建上下牙床绑定 Joint；
    - 创建上下牙床标准 Controller Hierarchy；
    - 使用 Matrix Network 建立 Controller Output -> Joint 驱动；
    - 对独立 Upper / Lower Teeth Model 创建单 Influence 刚性 SkinCluster；
    - 对一个 Gum Model 按 Connected Mesh Shell 自动分成 Upper / Lower 两组刚性权重；
    - 保留 Lower Teeth Controller Top Group，供后续 Jaw Component 接管 Follow。

重要边界：
    - Gum 自动权重只处理上下牙龈为两个或多个断开 Mesh Shell 的情况；
    - 每个 Gum Shell 会完整归属 Upper 或 Lower Teeth Joint，不使用 Maya 默认 Smooth Bind 猜权重；
    - 如果 Gum 是一整块连通拓扑，本 Component 会明确停止，不生成不可靠的自动权重；
    - 本 Component 不修改已有的未知 SkinCluster，避免破坏艺术家已有权重。
"""

from __future__ import print_function

import maya.api.OpenMaya as om
import maya.cmds as cmds

from ....core import joint_utils
from ....core import matrix_utils
from ....core import name_utils
from ....core import skin_utils
from ...controller import builder as controller_builder
from .. import config
from .. import face_base
from ..guide import FaceGuide


class TeethComponent(face_base.FaceBase):
    u"""Step 03 中的 Teeth Rig Component。"""

    def __init__(self):
        u"""初始化 Teeth Component。"""
        super(TeethComponent, self).__init__()

        self.face_guide = FaceGuide()

        # ---------------------------------------------------------------------
        # Guide
        # ---------------------------------------------------------------------
        self.upper_teeth_guide_name = None
        self.lower_teeth_guide_name = None
        self.upper_teeth_guide = None
        self.lower_teeth_guide = None

        # ---------------------------------------------------------------------
        # Build Name
        # ---------------------------------------------------------------------
        self.upper_teeth_jnt_name = None
        self.lower_teeth_jnt_name = None
        self.upper_teeth_ctrl_name = None
        self.lower_teeth_ctrl_name = None
        self.upper_teeth_matrix_name = None
        self.lower_teeth_matrix_name = None
        self.upper_teeth_skin_name = None
        self.lower_teeth_skin_name = None
        self.gum_skin_name = None

        # ---------------------------------------------------------------------
        # Controller Setting
        # ---------------------------------------------------------------------
        self.controller_global_scale = 1.0
        self.controller_color = 17
        self.controller_size = 1.0
        self.controller_radius = 1.0

        # ---------------------------------------------------------------------
        # Gum Weight Data
        # ---------------------------------------------------------------------
        self.gum_shell_data = []

        # ---------------------------------------------------------------------
        # Build Result
        # ---------------------------------------------------------------------
        self.upper_teeth_joint = None
        self.lower_teeth_joint = None

        self.upper_teeth_controller = None
        self.lower_teeth_controller = None

        self.upper_teeth_control = None
        self.lower_teeth_control = None
        self.upper_teeth_output = None
        self.lower_teeth_output = None
        self.upper_teeth_top_group = None
        self.lower_teeth_top_group = None

        self.upper_teeth_matrix_node = None
        self.lower_teeth_matrix_node = None

        self.upper_teeth_skin_cluster = None
        self.lower_teeth_skin_cluster = None
        self.gum_skin_cluster = None

    # =========================================================================
    # Input / Prepare
    # =========================================================================

    def collect_inputs(self):
        u"""
        收集并检查 Teeth Component 所需输入。

        Returns:
            bool:
                Setup、Guide 和 Controller Settings 全部读取成功后返回 True。
        """

        # =========================================================================
        # 步骤 1：检查 Step 01 Setup 数据
        # =========================================================================

        self.validate_setup_config(
            require_mouth_jnt_number=False
        )

        # =========================================================================
        # 步骤 2：动态生成必须的 Teeth Guide 名称
        # =========================================================================

        self.upper_teeth_guide_name = name_utils.Name.create_name(
            node_type="loc",
            side="md",
            part="upper_teeth",
            function="guide",
            index=1
        )

        self.lower_teeth_guide_name = name_utils.Name.create_name(
            node_type="loc",
            side="md",
            part="lower_teeth",
            function="guide",
            index=1
        )

        # =========================================================================
        # 步骤 3：获取并检查 Guide
        # =========================================================================

        self.upper_teeth_guide = self.face_guide.get_guide_node(
            self.upper_teeth_guide_name,
            required=True
        )

        self.lower_teeth_guide = self.face_guide.get_guide_node(
            self.lower_teeth_guide_name,
            required=True
        )

        # =========================================================================
        # 步骤 4：读取 Controller Settings
        # =========================================================================

        controller_settings = self.face_guide.load_controller_settings()

        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )

        self.controller_color = controller_settings.get(
            config.face_controller_color_attr_names["md"],
            17
        )

        self.controller_size = controller_settings.get(
            config.face_controller_size_attr_names["teeth"],
            1.0
        )

        return True

    def prepare_data(self):
        u"""
        准备 Teeth Joint / Controller 名称、层级和构建前检查数据。

        Returns:
            bool:
                命名、层级与构建前安全检查全部完成后返回 True。
        """

        # 确保 Face 的正式层级存在。
        self.ensure_hierarchy()

        # ---------------------------------------------------------------------
        # Joint Name
        # ---------------------------------------------------------------------
        self.upper_teeth_jnt_name = name_utils.Name.create_name(
            node_type="jnt",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )

        self.lower_teeth_jnt_name = name_utils.Name.create_name(
            node_type="jnt",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        # ---------------------------------------------------------------------
        # Controller Name
        # ---------------------------------------------------------------------
        self.upper_teeth_ctrl_name = name_utils.Name.create_name(
            node_type="ctrl",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )

        self.lower_teeth_ctrl_name = name_utils.Name.create_name(
            node_type="ctrl",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        # ---------------------------------------------------------------------
        # Rig Node Name
        # ---------------------------------------------------------------------
        self.upper_teeth_matrix_name = name_utils.Name.create_name(
            node_type="mult",
            side="md",
            part="upper_teeth",
            function="parent",
            index=1
        )

        self.lower_teeth_matrix_name = name_utils.Name.create_name(
            node_type="mult",
            side="md",
            part="lower_teeth",
            function="parent",
            index=1
        )

        self.upper_teeth_skin_name = name_utils.Name.create_name(
            node_type="skin",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )

        self.lower_teeth_skin_name = name_utils.Name.create_name(
            node_type="skin",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        self.gum_skin_name = name_utils.Name.create_name(
            node_type="skin",
            side="md",
            part="gum",
            function="bind",
            index=1
        )

        # ---------------------------------------------------------------------
        # Controller Radius
        # ---------------------------------------------------------------------
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(
                u"Teeth Controller Radius 必须大于 0。"
            )

        # ---------------------------------------------------------------------
        # Build 前安全检查
        # ---------------------------------------------------------------------
        self._validate_build_nodes_available()

        self._validate_model_skin_state(
            self.upper_teech_model,
            label=u"Upper Teeth Model"
        )

        self._validate_model_skin_state(
            self.lower_teech_model,
            label=u"Lower Teeth Model"
        )

        self._validate_model_skin_state(
            self.face_gum_model,
            label=u"Gum Model"
        )

        # Gum 的 Shell 分组和 Upper / Lower 判定必须在真正创建 Rig 前完成。
        # 这样拓扑不符合要求时，不会留下半套 Teeth Rig。
        self.gum_shell_data = self._prepare_gum_shell_data(
            self.face_gum_model
        )

        return True

    # =========================================================================
    # Build Validation
    # =========================================================================

    @staticmethod
    def _get_controller_hierarchy_names(control_name):
        u"""返回标准 Controller Builder 会创建的确定性节点名称。"""
        prefixes = [
            "ctrl",
            "offset",
            "connect",
            "space",
            "driven",
            "zero",
            "output",
        ]
        node_names = []

        for prefix in prefixes:
            if prefix == "ctrl":
                node_name = control_name
            else:
                if control_name.startswith("ctrl_"):
                    node_name = control_name.replace(
                        "ctrl_",
                        prefix + "_",
                        1
                    )
                else:
                    node_name = "{}_{}".format(
                        prefix,
                        control_name
                    )

            node_names.append(
                node_name
            )

        return node_names

    def _validate_build_nodes_available(self):
        u"""阻止旧 Teeth Rig 残留导致 Builder 静默生成带后缀的重复节点。"""
        expected_nodes = [
            self.upper_teeth_jnt_name,
            self.lower_teeth_jnt_name,
            self.upper_teeth_matrix_name,
            self.lower_teeth_matrix_name,
        ]

        if self.upper_teech_model:
            expected_nodes.append(
                self.upper_teeth_skin_name
            )

        if self.lower_teech_model:
            expected_nodes.append(
                self.lower_teeth_skin_name
            )

        if self.face_gum_model:
            expected_nodes.append(
                self.gum_skin_name
            )

        upper_control_nodes = self._get_controller_hierarchy_names(
            self.upper_teeth_ctrl_name
        )
        lower_control_nodes = self._get_controller_hierarchy_names(
            self.lower_teeth_ctrl_name
        )

        for node_name in upper_control_nodes:
            expected_nodes.append(
                node_name
            )

        for node_name in lower_control_nodes:
            expected_nodes.append(
                node_name
            )

        existing_nodes = []

        for node_name in expected_nodes:
            if not node_name:
                continue

            if not cmds.objExists(node_name):
                continue

            existing_nodes.append(
                node_name
            )

        if existing_nodes:
            raise RuntimeError(
                u"Teeth Rig 已存在或存在同名残留节点，请先清理后再构建：{}".format(
                    ", ".join(existing_nodes)
                )
            )

        return True

    @staticmethod
    def _validate_model_skin_state(model, label):
        u"""构建前拒绝覆盖模型上已经存在的未知 SkinCluster。"""
        if not model:
            return True

        skin_cluster = skin_utils.find_skin_cluster(
            model
        )

        if not skin_cluster:
            return True

        raise RuntimeError(
            u"{} 已经存在 SkinCluster：{}。Teeth Component 不会自动覆盖已有权重。".format(
                label,
                skin_cluster
            )
        )

    # =========================================================================
    # Gum Geometry / Weight Preparation
    # =========================================================================

    @staticmethod
    def _get_mesh_shape(model):
        u"""返回 Gum Model 唯一的非 Intermediate Mesh Shape。"""
        if not model:
            return None

        mesh_shapes = cmds.listRelatives(
            model,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="mesh"
        )

        if mesh_shapes is None:
            mesh_shapes = []

        if len(mesh_shapes) != 1:
            raise RuntimeError(
                u"Gum Model 必须包含且只包含一个有效 Mesh Shape：{} | shapes={}".format(
                    model,
                    len(mesh_shapes)
                )
            )

        return mesh_shapes[0]

    @staticmethod
    def _distance_squared(point_a, point_b):
        u"""返回两个三维点之间的平方距离。"""
        delta_x = point_a[0] - point_b[0]
        delta_y = point_a[1] - point_b[1]
        delta_z = point_a[2] - point_b[2]

        return (
            delta_x * delta_x +
            delta_y * delta_y +
            delta_z * delta_z
        )

    def _get_mesh_shell_data(self, model):
        u"""使用 Maya API 读取模型 Connected Vertex Shell 及世界空间中心。"""
        mesh_shape = self._get_mesh_shape(
            model
        )

        selection = om.MSelectionList()
        selection.add(
            mesh_shape
        )
        mesh_path = selection.getDagPath(
            0
        )

        mesh_function = om.MFnMesh(
            mesh_path
        )
        world_points = mesh_function.getPoints(
            om.MSpace.kWorld
        )

        # 先完整建立 Vertex 邻接表，再用普通 BFS 分 Shell。
        adjacency = {}
        vertex_iterator = om.MItMeshVertex(
            mesh_path
        )

        while not vertex_iterator.isDone():
            vertex_index = vertex_iterator.index()
            connected_vertices = vertex_iterator.getConnectedVertices()

            adjacency[vertex_index] = []

            for connected_vertex in connected_vertices:
                adjacency[vertex_index].append(
                    connected_vertex
                )

            vertex_iterator.next()

        visited_vertices = set()
        shell_data = []
        vertex_count = mesh_function.numVertices
        vertex_index = 0

        while vertex_index < vertex_count:
            if vertex_index in visited_vertices:
                vertex_index += 1
                continue

            stack = [
                vertex_index
            ]
            shell_vertices = []

            while stack:
                current_vertex = stack.pop()

                if current_vertex in visited_vertices:
                    continue

                visited_vertices.add(
                    current_vertex
                )
                shell_vertices.append(
                    current_vertex
                )

                connected_vertices = adjacency.get(
                    current_vertex,
                    []
                )

                for connected_vertex in connected_vertices:
                    if connected_vertex in visited_vertices:
                        continue

                    stack.append(
                        connected_vertex
                    )

            center_x = 0.0
            center_y = 0.0
            center_z = 0.0

            for shell_vertex in shell_vertices:
                point = world_points[shell_vertex]
                center_x += point.x
                center_y += point.y
                center_z += point.z

            shell_vertex_count = len(
                shell_vertices
            )

            if shell_vertex_count <= 0:
                vertex_index += 1
                continue

            shell_center = [
                center_x / shell_vertex_count,
                center_y / shell_vertex_count,
                center_z / shell_vertex_count,
            ]

            shell_data.append({
                "vertices": shell_vertices,
                "center": shell_center,
                "side": None,
            })

            vertex_index += 1

        return shell_data

    def _prepare_gum_shell_data(self, model):
        u"""按 Connected Shell 中心到上下 Teeth Guide 的距离预分类 Gum 权重。"""
        if not model:
            return []

        shell_data = self._get_mesh_shell_data(
            model
        )

        if len(shell_data) < 2:
            raise RuntimeError(
                u"Gum Model 至少需要两个断开的 Mesh Shell 才能自动区分上下牙龈：{}".format(
                    model
                )
            )

        upper_position = cmds.xform(
            self.upper_teeth_guide,
            query=True,
            worldSpace=True,
            translation=True
        )
        lower_position = cmds.xform(
            self.lower_teeth_guide,
            query=True,
            worldSpace=True,
            translation=True
        )

        upper_shell_count = 0
        lower_shell_count = 0

        for shell in shell_data:
            shell_center = shell["center"]

            upper_distance = self._distance_squared(
                shell_center,
                upper_position
            )
            lower_distance = self._distance_squared(
                shell_center,
                lower_position
            )

            if upper_distance <= lower_distance:
                shell["side"] = "upper"
                upper_shell_count += 1
            else:
                shell["side"] = "lower"
                lower_shell_count += 1

        if upper_shell_count == 0 or lower_shell_count == 0:
            raise RuntimeError(
                u"Gum Shell 自动分类失败，必须至少存在一组 Upper 和一组 Lower Shell。"
            )

        return shell_data

    # =========================================================================
    # Joint
    # =========================================================================

    def create_joint(self):
        u"""
        根据 Teeth Guide 创建上下牙床绑定 Joint。

        Returns:
            list[str]:
                按 Upper、Lower 顺序返回创建完成的两个 Joint。
        """
        joint_radius = self.controller_radius * 0.25

        self.upper_teeth_joint = joint_utils.Joint.create_at_object(
            obj=self.upper_teeth_guide,
            name=self.upper_teeth_jnt_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=joint_radius
        )

        self.lower_teeth_joint = joint_utils.Joint.create_at_object(
            obj=self.lower_teeth_guide,
            name=self.lower_teeth_jnt_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=joint_radius
        )

        return [
            self.upper_teeth_joint,
            self.lower_teeth_joint,
        ]

    # =========================================================================
    # Controller
    # =========================================================================

    def create_controller(self):
        u"""
        创建上下牙床对应的标准 Controller Hierarchy。

        Returns:
            list[dict]:
                按 Upper、Lower 顺序返回 Controller Builder 的结果字典。
        """
        self.upper_teeth_controller = controller_builder.create_controller(
            name=self.upper_teeth_ctrl_name,
            shape="circle",
            radius=self.controller_radius,
            axis="Z+",
            target=self.upper_teeth_guide,
            parent=self.face_ctrl_grp,
            color=self.controller_color,
            create_sub_control=False,
            create_extra_groups=True,
            add_to_set=True,
            control_set=config.face_ctrl_set
        )

        self.lower_teeth_controller = controller_builder.create_controller(
            name=self.lower_teeth_ctrl_name,
            shape="circle",
            radius=self.controller_radius,
            axis="Z+",
            target=self.lower_teeth_guide,
            parent=self.face_ctrl_grp,
            color=self.controller_color,
            create_sub_control=False,
            create_extra_groups=True,
            add_to_set=True,
            control_set=config.face_ctrl_set
        )

        self.upper_teeth_control = self.upper_teeth_controller["control"]
        self.lower_teeth_control = self.lower_teeth_controller["control"]

        self.upper_teeth_output = self.upper_teeth_controller["output"]
        self.lower_teeth_output = self.lower_teeth_controller["output"]

        self.upper_teeth_top_group = self.upper_teeth_controller["top_group"]
        self.lower_teeth_top_group = self.lower_teeth_controller["top_group"]

        return [
            self.upper_teeth_controller,
            self.lower_teeth_controller,
        ]

    # =========================================================================
    # Connection
    # =========================================================================

    def create_connection(self):
        u"""
        建立 Teeth Controller、Joint、独立牙齿模型和 Gum 的驱动关系。

        Returns:
            bool:
                Matrix 驱动、牙齿刚性 Skin 与可选 Gum Shell Skin 全部完成后返回 True。
        """

        # ---------------------------------------------------------------------
        # Controller Output -> Joint
        # ---------------------------------------------------------------------
        self.upper_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.upper_teeth_output,
            driven=self.upper_teeth_joint,
            maintain_offset=False,
            name=self.upper_teeth_matrix_name
        )

        self.lower_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.lower_teeth_output,
            driven=self.lower_teeth_joint,
            maintain_offset=False,
            name=self.lower_teeth_matrix_name
        )

        # ---------------------------------------------------------------------
        # Joint -> Teeth Model
        # ---------------------------------------------------------------------
        self.upper_teeth_skin_cluster = self._create_rigid_skin_cluster(
            model=self.upper_teech_model,
            joint=self.upper_teeth_joint,
            skin_name=self.upper_teeth_skin_name
        )

        self.lower_teeth_skin_cluster = self._create_rigid_skin_cluster(
            model=self.lower_teech_model,
            joint=self.lower_teeth_joint,
            skin_name=self.lower_teeth_skin_name
        )

        # ---------------------------------------------------------------------
        # Upper + Lower Joint -> Gum Model
        # ---------------------------------------------------------------------
        self.gum_skin_cluster = self._create_gum_skin_cluster(
            model=self.face_gum_model,
            upper_joint=self.upper_teeth_joint,
            lower_joint=self.lower_teeth_joint,
            skin_name=self.gum_skin_name,
            shell_data=self.gum_shell_data
        )

        return True

    @staticmethod
    def _create_rigid_skin_cluster(
            model,
            joint,
            skin_name
    ):
        u"""使用单个 Joint 创建全权重为 1 的刚性 SkinCluster。"""
        if not model:
            return None

        existing_skin_cluster = skin_utils.find_skin_cluster(
            model
        )

        if existing_skin_cluster:
            raise RuntimeError(
                u"模型已经存在 SkinCluster：{}".format(
                    existing_skin_cluster
                )
            )

        skin_result = cmds.skinCluster(
            joint,
            model,
            name=skin_name,
            toSelectedBones=True,
            bindMethod=0,
            skinMethod=0,
            normalizeWeights=1,
            maximumInfluences=1,
            obeyMaxInfluences=True
        )

        if not skin_result:
            raise RuntimeError(
                u"创建 Teeth SkinCluster 失败：{}".format(
                    model
                )
            )

        return skin_result[0]

    @staticmethod
    def _create_gum_skin_cluster(
            model,
            upper_joint,
            lower_joint,
            skin_name,
            shell_data
    ):
        u"""创建双 Influence Gum SkinCluster，并把每个 Connected Shell 刚性分配给一侧。"""
        if not model:
            return None

        if not shell_data:
            raise RuntimeError(
                u"没有可用于 Gum 绑定的 Shell 数据。"
            )

        existing_skin_cluster = skin_utils.find_skin_cluster(
            model
        )

        if existing_skin_cluster:
            raise RuntimeError(
                u"Gum Model 已经存在 SkinCluster：{}".format(
                    existing_skin_cluster
                )
            )

        skin_result = cmds.skinCluster(
            [
                upper_joint,
                lower_joint,
            ],
            model,
            name=skin_name,
            toSelectedBones=True,
            bindMethod=0,
            skinMethod=0,
            normalizeWeights=1,
            maximumInfluences=1,
            obeyMaxInfluences=True
        )

        if not skin_result:
            raise RuntimeError(
                u"创建 Gum SkinCluster 失败：{}".format(
                    model
                )
            )

        skin_cluster = skin_result[0]

        for shell in shell_data:
            vertex_components = []

            for vertex_index in shell["vertices"]:
                vertex_components.append(
                    "{}.vtx[{}]".format(
                        model,
                        vertex_index
                    )
                )

            if shell["side"] == "upper":
                transform_values = [
                    (upper_joint, 1.0),
                    (lower_joint, 0.0),
                ]
            elif shell["side"] == "lower":
                transform_values = [
                    (upper_joint, 0.0),
                    (lower_joint, 1.0),
                ]
            else:
                raise RuntimeError(
                    u"Gum Shell 没有 Upper / Lower 分类结果。"
                )

            cmds.skinPercent(
                skin_cluster,
                vertex_components,
                transformValue=transform_values,
                normalize=True
            )

        return skin_cluster

    # =========================================================================
    # Finalize
    # =========================================================================

    def finalize_step(self):
        u"""
        检查 Teeth Component 最终结果并整理显示 / Metadata。

        Returns:
            bool:
                必须节点及可选牙齿 / Gum Skin 结果全部有效时返回 True。
        """
        required_nodes = [
            self.upper_teeth_joint,
            self.lower_teeth_joint,
            self.upper_teeth_control,
            self.lower_teeth_control,
            self.upper_teeth_output,
            self.lower_teeth_output,
            self.upper_teeth_matrix_node,
            self.lower_teeth_matrix_node,
        ]

        for node in required_nodes:
            if not node:
                raise RuntimeError(
                    u"Teeth Component 构建结果不完整。"
                )

            if not cmds.objExists(node):
                raise RuntimeError(
                    u"Teeth Component 构建节点不存在：{}".format(
                        node
                    )
                )

        if self.upper_teech_model:
            if not self.upper_teeth_skin_cluster:
                raise RuntimeError(
                    u"Upper Teeth Model 没有完成刚性 Skin 绑定。"
                )

            if not cmds.objExists(self.upper_teeth_skin_cluster):
                raise RuntimeError(
                    u"Upper Teeth SkinCluster 不存在：{}".format(
                        self.upper_teeth_skin_cluster
                    )
                )

        if self.lower_teech_model:
            if not self.lower_teeth_skin_cluster:
                raise RuntimeError(
                    u"Lower Teeth Model 没有完成刚性 Skin 绑定。"
                )

            if not cmds.objExists(self.lower_teeth_skin_cluster):
                raise RuntimeError(
                    u"Lower Teeth SkinCluster 不存在：{}".format(
                        self.lower_teeth_skin_cluster
                    )
                )

        if self.face_gum_model:
            if not self.gum_skin_cluster:
                raise RuntimeError(
                    u"Gum Model 没有完成 Upper / Lower Shell Skin 绑定。"
                )

            if not cmds.objExists(self.gum_skin_cluster):
                raise RuntimeError(
                    u"Gum SkinCluster 不存在：{}".format(
                        self.gum_skin_cluster
                    )
                )

        return True


__all__ = [
    "TeethComponent",
]
