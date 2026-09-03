# coding=utf-8
from pathlib import Path


def replace_once(text, old_text, new_text, label):
    if old_text not in text:
        raise RuntimeError("Missing patch anchor: {}".format(label))

    return text.replace(old_text, new_text, 1)


# =============================================================================
# Config: bump formal Face Guide schema version
# =============================================================================
config_path = Path("systems/face/config.py")
config_text = config_path.read_text(encoding="utf-8")
config_text = replace_once(
    config_text,
    'face_guide_version = "1.0"',
    'face_guide_version = "1.1"',
    "face guide version"
)
config_path.write_text(config_text, encoding="utf-8")


# =============================================================================
# FaceGuide: generated Cheek guide schema + creation + ordered query
# =============================================================================
face_guide_path = Path("systems/face/guide/face_guide.py")
face_guide_text = face_guide_path.read_text(encoding="utf-8")

face_guide_text = replace_once(
    face_guide_text,
    '''    mirror_sides = [\n        "lf",\n        "rt",\n    ]\n\n    zero_attributes = [''',
    '''    mirror_sides = [\n        "lf",\n        "rt",\n    ]\n\n    cheek_regions = [\n        "cheekbone",\n        "nasolabial",\n        "cheek",\n    ]\n\n    cheek_region_counts = {\n        "cheekbone": 3,\n        "nasolabial": 3,\n        "cheek": 2,\n    }\n\n    zero_attributes = [''',
    "cheek class schema"
)

face_guide_text = replace_once(
    face_guide_text,
    '''        if not self.guide_exists():\n            raise RuntimeError(\n                u"Face Guide 尚未完整加载，请重新导入模板后再继续。"\n            )\n\n        return True''',
    '''        if not self.guide_exists():\n            raise RuntimeError(\n                u"Face Guide 尚未完整加载，请重新导入模板后再继续。"\n            )\n\n        # -------------------------------------------------------------------------\n        # Step 02：升级旧 Guide 场景时补齐正式 Cheek Guide Schema\n        # -------------------------------------------------------------------------\n        self.ensure_cheek_guides()\n\n        return True''',
    "collect inputs cheek upgrade"
)

face_guide_text = replace_once(
    face_guide_text,
    '''        for locator_name in matches:\n            if locator_name in locator_names:\n                continue\n\n            locator_names.append(\n                locator_name\n            )\n\n        # -------------------------------------------------------------------------\n        # Step 04：检查当前条件与边界情况，并进入对应处理分支\n        # -------------------------------------------------------------------------\n        if not locator_names:''',
    '''        for locator_name in matches:\n            if locator_name in locator_names:\n                continue\n\n            locator_names.append(\n                locator_name\n            )\n\n        # -------------------------------------------------------------------------\n        # Step 04：把代码生成的 Cheek Locator 作为正式 Template Schema 的一部分\n        # -------------------------------------------------------------------------\n        generated_locator_names = self.get_generated_template_locator_names()\n\n        for locator_name in generated_locator_names:\n            if locator_name in locator_names:\n                continue\n\n            locator_names.append(\n                locator_name\n            )\n\n        # -------------------------------------------------------------------------\n        # Step 05：检查当前条件与边界情况，并进入对应处理分支\n        # -------------------------------------------------------------------------\n        if not locator_names:''',
    "template generated locator names"
)

face_guide_text = replace_once(
    face_guide_text,
    '''        if self.guide_exists():\n            return {\n                "imported": False,\n                "guide_root": self.guide_root,\n                "guide_move_ctrl": self.guide_move_ctrl,\n                "new_nodes": [],\n            }''',
    '''        if self.guide_exists():\n            cheek_guide_result = self.ensure_cheek_guides()\n\n            if cheek_guide_result["created_count"] > 0:\n                self.apply_mirror(\n                    source_side="lf",\n                    target_side="rt"\n                )\n                self.save_guide_config()\n                self.set_step_completed(\n                    completed=False\n                )\n                self.invalidate_later_steps()\n\n            return {\n                "imported": False,\n                "guide_root": self.guide_root,\n                "guide_move_ctrl": self.guide_move_ctrl,\n                "new_nodes": [],\n                "cheek_guide": cheek_guide_result,\n            }''',
    "existing guide upgrade"
)

face_guide_text = replace_once(
    face_guide_text,
    '''        if not self.guide_exists():\n            raise RuntimeError(\n                u"Face Guide 模板导入完成，但没有找到 {}。".format(\n                    self.guide_move_ctrl_name\n                )\n            )\n\n        # -------------------------------------------------------------------------\n        # Step 04：应用并更新当前阶段需要的属性或状态\n        # -------------------------------------------------------------------------\n        self.apply_mirror(''',
    '''        if not self.guide_exists():\n            raise RuntimeError(\n                u"Face Guide 模板导入完成，但没有找到 {}。".format(\n                    self.guide_move_ctrl_name\n                )\n            )\n\n        # -------------------------------------------------------------------------\n        # Step 04：在正式模板上补齐程序化 Cheek Guide，再统一执行左右 Mirror\n        # -------------------------------------------------------------------------\n        cheek_guide_result = self.ensure_cheek_guides()\n\n        self.apply_mirror(''',
    "fresh guide cheek extension"
)

face_guide_text = replace_once(
    face_guide_text,
    '''            "guide_move_ctrl": self.guide_move_ctrl,\n            "new_nodes": imported_nodes,\n        }''',
    '''            "guide_move_ctrl": self.guide_move_ctrl,\n            "new_nodes": imported_nodes,\n            "cheek_guide": cheek_guide_result,\n        }''',
    "fresh guide return cheek result"
)

cheek_methods = r'''
    def get_generated_template_locator_names(self):
        u"""
        返回由 FaceGuide 代码生成、但属于正式 Template Schema 的 Locator 名称。

        当前只包含 Cheek：每侧 3 个 CheekBone、3 个 Nasolabial、2 个 Cheek。

        Returns:
            list[str]:
                固定顺序的程序化 Face Guide Locator 名称。
        """
        locator_names = []

        # -------------------------------------------------------------------------
        # Step 01：按 Side / Region / Index 创建稳定的正式 Guide 名称
        # -------------------------------------------------------------------------
        for side in self.mirror_sides:
            for region in self.cheek_regions:
                region_count = self.cheek_region_counts[region]
                index = 1

                while index <= region_count:
                    locator_names.append(
                        self._create_guide_name(
                            side,
                            region,
                            index
                        )
                    )
                    index += 1

        return locator_names

    @staticmethod
    def _blend_position(
            start_position,
            end_position,
            weight
    ):
        u"""按线性权重在两个世界坐标之间插值。"""
        weight = float(weight)
        inverse_weight = 1.0 - weight

        return [
            start_position[0] * inverse_weight + end_position[0] * weight,
            start_position[1] * inverse_weight + end_position[1] * weight,
            start_position[2] * inverse_weight + end_position[2] * weight,
        ]

    def _get_cheek_initial_positions(self):
        u"""根据当前 Eye / Lid / Nose / Mouth Landmark 计算 LF Cheek 初始位置。"""
        # -------------------------------------------------------------------------
        # Step 01：读取当前模板已有的左侧 Landmark
        # -------------------------------------------------------------------------
        eye_ball = self.get_guide_node(
            self._create_guide_name("lf", "eye_ball", 1),
            required=True
        )
        outer_lid = self.get_guide_node(
            self._create_guide_name("lf", "outer_lid", 1),
            required=True
        )
        nose_side = self.get_guide_node(
            self._create_guide_name("lf", "nose_side", 1),
            required=True
        )
        mouth_corner = self.get_guide_node(
            self._create_guide_name("lf", "mouth_corner", 1),
            required=True
        )

        eye_position = transform_utils.get_world_translation(
            eye_ball
        )
        outer_lid_position = transform_utils.get_world_translation(
            outer_lid
        )
        nose_position = transform_utils.get_world_translation(
            nose_side
        )
        mouth_position = transform_utils.get_world_translation(
            mouth_corner
        )

        # -------------------------------------------------------------------------
        # Step 02：沿眼下 / 颧骨区域生成三个 CheekBone 初始位置
        # -------------------------------------------------------------------------
        cheekbone_positions = [
            self._blend_position(
                nose_position,
                outer_lid_position,
                0.55
            ),
            self._blend_position(
                eye_position,
                mouth_position,
                0.32
            ),
            self._blend_position(
                outer_lid_position,
                mouth_position,
                0.48
            ),
        ]

        # -------------------------------------------------------------------------
        # Step 03：沿 Nose Side 到 Mouth Corner 生成三段 Nasolabial 初始位置
        # -------------------------------------------------------------------------
        nasolabial_positions = [
            self._blend_position(
                nose_position,
                mouth_position,
                0.25
            ),
            self._blend_position(
                nose_position,
                mouth_position,
                0.50
            ),
            self._blend_position(
                nose_position,
                mouth_position,
                0.75
            ),
        ]

        # -------------------------------------------------------------------------
        # Step 04：在 CheekBone 与 Nasolabial 之间生成两个主 Cheek 初始位置
        # -------------------------------------------------------------------------
        cheek_positions = [
            self._blend_position(
                cheekbone_positions[1],
                nasolabial_positions[1],
                0.50
            ),
            self._blend_position(
                cheekbone_positions[2],
                nasolabial_positions[2],
                0.50
            ),
        ]

        return {
            "cheekbone": cheekbone_positions,
            "nasolabial": nasolabial_positions,
            "cheek": cheek_positions,
        }

    def _ensure_cheek_guide_group(self):
        u"""创建或返回正式 Cheek Guide Group。"""
        group_name = self.create_name(
            type="grp",
            side="md",
            part="cheek",
            function="guide",
            index=1
        )
        group_node = self.get_guide_node(
            group_name,
            required=False
        )

        if group_node:
            return group_node

        self.refresh_guide_handles()

        if not self.guide_move_ctrl:
            raise RuntimeError(
                u"创建 Cheek Guide 前必须存在 Face Guide Move Ctrl。"
            )

        return scene_utils.create_node(
            "transform",
            ":{}".format(group_name),
            parent=self.guide_move_ctrl
        )

    def _ensure_cheek_locator(
            self,
            side,
            region,
            index,
            parent_group,
            world_position=None
    ):
        u"""创建或返回一个 Cheek Zero + Locator + LocatorShape。"""
        zero_name = self.create_name(
            type="zero",
            side=side,
            part=region,
            function="guide",
            index=index
        )
        locator_name = self._create_guide_name(
            side,
            region,
            index
        )

        zero_node = self.get_guide_node(
            zero_name,
            required=False
        )
        locator_node = self.get_guide_node(
            locator_name,
            required=False
        )
        created_zero = False
        created_locator = False

        # -------------------------------------------------------------------------
        # Step 01：只创建缺失 Zero，并在首次创建时写入初始化世界位置
        # -------------------------------------------------------------------------
        if not zero_node:
            zero_node = scene_utils.create_node(
                "transform",
                ":{}".format(zero_name),
                parent=parent_group
            )
            created_zero = True

            if world_position is not None:
                transform_utils.set_world_translation(
                    zero_node,
                    world_position
                )

        # -------------------------------------------------------------------------
        # Step 02：创建可编辑 Locator Transform 和 Locator Shape
        # -------------------------------------------------------------------------
        if not locator_node:
            locator_node = scene_utils.create_node(
                "transform",
                ":{}".format(locator_name),
                parent=zero_node
            )
            locator_shape = cmds.createNode(
                "locator",
                name=":{}Shape".format(locator_name),
                parent=locator_node
            )
            cmds.setAttr(
                locator_shape + ".overrideEnabled",
                1
            )
            cmds.setAttr(
                locator_shape + ".overrideColor",
                18
            )
            cmds.setAttr(
                locator_shape + ".localScaleX",
                2.0
            )
            cmds.setAttr(
                locator_shape + ".localScaleY",
                2.0
            )
            cmds.setAttr(
                locator_shape + ".localScaleZ",
                2.0
            )
            created_locator = True

        # -------------------------------------------------------------------------
        # Step 03：Zero 只保存初始化空间，Animator / Rigger 只编辑 Locator
        # -------------------------------------------------------------------------
        for attribute in self.zero_attributes:
            plug = "{}.{}".format(
                zero_node,
                attribute
            )

            if not cmds.objExists(plug):
                continue

            cmds.setAttr(
                plug,
                lock=True
            )

        return {
            "zero": zero_node,
            "locator": locator_node,
            "created_zero": created_zero,
            "created_locator": created_locator,
        }

    def _initialize_mirrored_cheek_zero(
            self,
            source_zero,
            target_zero
    ):
        u"""按当前 Face Mirror 规则初始化一个新建的 RT Cheek Zero。"""
        # -------------------------------------------------------------------------
        # Step 01：根级 Cheek Zero 在共同 Parent 下沿 X 轴镜像
        # -------------------------------------------------------------------------
        self.set_attr_preserve_lock(
            target_zero,
            "translateX",
            -cmds.getAttr(source_zero + ".translateX")
        )
        self.set_attr_preserve_lock(
            target_zero,
            "translateY",
            cmds.getAttr(source_zero + ".translateY")
        )
        self.set_attr_preserve_lock(
            target_zero,
            "translateZ",
            cmds.getAttr(source_zero + ".translateZ")
        )
        self.set_attr_preserve_lock(
            target_zero,
            "scaleX",
            -cmds.getAttr(source_zero + ".scaleX")
        )
        return True

    def ensure_cheek_guides(self):
        u"""
        确保正式 Face Guide 中存在完整 Cheek Guide Schema。

        Cheek 初始位置由当前 Eye / Outer Lid / Nose Side / Mouth Corner 自动推导，
        因此不会依赖固定世界坐标。已经存在的 Cheek Guide 不会被覆盖。

        Returns:
            dict:
                Cheek Guide Group、创建数量和固定 Region Count。

        Raises:
            RuntimeError:
                Face Guide 或初始化 Landmark 不完整时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：确认 Guide 已加载，并准备 Cheek Group / 初始位置
        # -------------------------------------------------------------------------
        if not self.guide_exists():
            raise RuntimeError(
                u"创建 Cheek Guide 前必须先加载 Face Guide。"
            )

        cheek_group = self._ensure_cheek_guide_group()
        initial_positions = self._get_cheek_initial_positions()
        created_count = 0

        # -------------------------------------------------------------------------
        # Step 02：逐 Region 创建 LF Source，再创建同名 RT Mirror Pair
        # -------------------------------------------------------------------------
        for region in self.cheek_regions:
            region_count = self.cheek_region_counts[region]
            index = 1

            while index <= region_count:
                lf_result = self._ensure_cheek_locator(
                    side="lf",
                    region=region,
                    index=index,
                    parent_group=cheek_group,
                    world_position=initial_positions[region][index - 1]
                )
                rt_result = self._ensure_cheek_locator(
                    side="rt",
                    region=region,
                    index=index,
                    parent_group=cheek_group,
                    world_position=None
                )

                if lf_result["created_locator"]:
                    created_count += 1

                if rt_result["created_locator"]:
                    created_count += 1

                if rt_result["created_zero"]:
                    self._initialize_mirrored_cheek_zero(
                        lf_result["zero"],
                        rt_result["zero"]
                    )

                index += 1

        # -------------------------------------------------------------------------
        # Step 03：返回稳定 Schema，供 Build / Reimport / Runtime Test 复用
        # -------------------------------------------------------------------------
        return {
            "group": cheek_group,
            "created_count": created_count,
            "region_counts": dict(self.cheek_region_counts),
        }

    def get_cheek_guides(self, required=True):
        u"""
        返回左右 CheekBone / Nasolabial / Cheek 的固定有序 Guide。

        Args:
            required (bool):
                缺少任意正式 Cheek Guide 时是否直接抛出异常。

        Returns:
            dict:
                ``{side: {region: [guide, ...]}}`` 固定结构。
        """
        result = {}

        # -------------------------------------------------------------------------
        # Step 01：按正式 Schema 顺序解析每侧每个 Region 的 Guide
        # -------------------------------------------------------------------------
        for side in self.mirror_sides:
            region_dict = {}

            for region in self.cheek_regions:
                guide_names = []
                region_count = self.cheek_region_counts[region]
                index = 1

                while index <= region_count:
                    guide_names.append(
                        self._create_guide_name(
                            side,
                            region,
                            index
                        )
                    )
                    index += 1

                region_dict[region] = self.get_guides_from_names(
                    guide_names,
                    required=required
                )

            result[side] = region_dict

        return result

'''

face_guide_text = replace_once(
    face_guide_text,
    '''    def get_lip_guides(self, required=True):''',
    cheek_methods + '''    def get_lip_guides(self, required=True):''',
    "insert cheek guide methods"
)

face_guide_path.write_text(face_guide_text, encoding="utf-8")


# =============================================================================
# CheekModule: consume one explicit structured FaceGuide API
# =============================================================================
cheek_path = Path("systems/face/modules/cheek.py")
cheek_text = cheek_path.read_text(encoding="utf-8")

cheek_text = cheek_text.replace(
    u'''当前正式 Face Guide 模板尚未包含 Cheek / CheekBone / Nasolabial 定位时，\n本模块不会阻塞完整 FaceRig，而是明确返回 skipped 状态。Guide 一旦补齐，\n同一套 Module 会自动进入正常创建流程。''',
    u'''正式 Face Guide 由 FaceGuide 统一维护 CheekBone / Nasolabial / Cheek 定位；\n本模块只消费结构化 Guide 数据，不再维护独立 bpjnt 或额外定位资产。'''
)

old_load_block = '''        # -------------------------------------------------------------------------\n        # Step 01：逐侧、逐区域收集 Guide，并建立后续 Jnt/Ctrl/Matrix 的统一数据容器\n        # -------------------------------------------------------------------------\n        total_guide_count = 0\n\n        for side in self.sides:\n            region_dict = {}\n\n            for region in self.regions:\n                region_guides = self.face_guide.get_part_guides(\n                    part=region,\n                    side=side,\n                    required=False\n                )\n                region_dict[region] = {\n                    "guides": list(region_guides),\n                    "jnts": [],\n                    "ctrl_dict_list": [],\n                    "matrix_nodes": [],\n                }\n                total_guide_count += len(region_guides)\n\n            self.cheek_side_dict[side]["region_dict"] = region_dict\n'''

new_load_block = '''        # -------------------------------------------------------------------------\n        # Step 01：通过 FaceGuide 的固定 Schema 一次性读取左右 Cheek Guide\n        # -------------------------------------------------------------------------\n        cheek_guide_dict = self.face_guide.get_cheek_guides(\n            required=True\n        )\n        total_guide_count = 0\n\n        for side in self.sides:\n            region_dict = {}\n\n            for region in self.regions:\n                region_guides = cheek_guide_dict[side][region]\n                region_dict[region] = {\n                    "guides": list(region_guides),\n                    "jnts": [],\n                    "ctrl_dict_list": [],\n                    "matrix_nodes": [],\n                }\n                total_guide_count += len(region_guides)\n\n            self.cheek_side_dict[side]["region_dict"] = region_dict\n'''

cheek_text = replace_once(
    cheek_text,
    old_load_block,
    new_load_block,
    "CheekModule structured guide query"
)
cheek_path.write_text(cheek_text, encoding="utf-8")


# =============================================================================
# Existing long-term static contract: lock Cheek Guide architecture in place
# =============================================================================
contract_path = Path("tests/face_modules_maya2023_smoke_contract_test.py")
contract_text = contract_path.read_text(encoding="utf-8")

contract_text = replace_once(
    contract_text,
    '''SMOKE_PATH = os.path.join(\n    TESTS_DIR,\n    "face_modules_maya2023_smoke_test.py"\n)\n''',
    '''SMOKE_PATH = os.path.join(\n    TESTS_DIR,\n    "face_modules_maya2023_smoke_test.py"\n)\n\nPACKAGE_ROOT = os.path.dirname(\n    TESTS_DIR\n)\n\nFACE_GUIDE_PATH = os.path.join(\n    PACKAGE_ROOT,\n    "systems",\n    "face",\n    "guide",\n    "face_guide.py"\n)\n\nCHEEK_MODULE_PATH = os.path.join(\n    PACKAGE_ROOT,\n    "systems",\n    "face",\n    "modules",\n    "cheek.py"\n)\n''',
    "contract cheek paths"
)

contract_text = replace_once(
    contract_text,
    '''    with open(SMOKE_PATH, "r", encoding="utf-8") as file_object:\n        source = file_object.read()\n\n    module_tree = ast.parse(''',
    '''    with open(SMOKE_PATH, "r", encoding="utf-8") as file_object:\n        source = file_object.read()\n\n    with open(FACE_GUIDE_PATH, "r", encoding="utf-8") as file_object:\n        face_guide_source = file_object.read()\n\n    with open(CHEEK_MODULE_PATH, "r", encoding="utf-8") as file_object:\n        cheek_module_source = file_object.read()\n\n    module_tree = ast.parse(''',
    "contract read cheek sources"
)

contract_text = replace_once(
    contract_text,
    '''    print(\n        u"Face Modules Maya 2023 Smoke Contract: PASS"\n    )''',
    '''    # -------------------------------------------------------------------------\n    # Step 06：Cheek 必须使用 FaceGuide 正式生成 Schema，而不是再次退回可选空模块\n    # -------------------------------------------------------------------------\n    cheek_contract_text_list = [\n        "cheek_region_counts",\n        "def get_generated_template_locator_names",\n        "def ensure_cheek_guides",\n        "def get_cheek_guides",\n    ]\n\n    for required_text in cheek_contract_text_list:\n        if required_text in face_guide_source:\n            continue\n\n        raise AssertionError(\n            u"FaceGuide 缺少 Cheek Guide 契约：{}".format(\n                required_text\n            )\n        )\n\n    if "self.face_guide.get_cheek_guides(" not in cheek_module_source:\n        raise AssertionError(\n            u"CheekModule 必须通过 FaceGuide.get_cheek_guides() 读取正式定位。"\n        )\n\n    print(\n        u"Face Modules Maya 2023 Smoke Contract: PASS"\n    )''',
    "contract cheek architecture checks"
)

contract_path.write_text(contract_text, encoding="utf-8")

print("Cheek guide extension migration applied.")
