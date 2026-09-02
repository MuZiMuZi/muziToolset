# Runtime 中文步骤注释审计

> 本文件由 `scripts/audit_runtime_step_comments.py` 自动生成。

扫描 Runtime Python 文件：**97**

需要补充步骤注释的复杂函数：**290**

## `app/toolbox.py`

- `ToolCard.__init__` — L257，45 行，控制流 0，Call 11
- `ToolCard.create_widgets` — L303，41 行，控制流 2，Call 15
- `ToolCard.create_layouts` — L345，27 行，控制流 0，Call 19
- `ToolSection.__init__` — L436，47 行，控制流 0，Call 24
- `CategoryPage.create_layouts` — L610，32 行，控制流 0，Call 20
- `RiggingToolbox.create_widgets` — L789，72 行，控制流 0，Call 37
- `RiggingToolbox.create_layouts` — L862，44 行，控制流 0，Call 33
- `RiggingToolbox.rebuild_tools` — L945，75 行，控制流 7，Call 23
## `app/window_manager.py`

- `_is_new_tool_window` — L110，21 行，控制流 6，Call 4
- `_find_new_top_level_window` — L133，37 行，控制流 10，Call 6
- `_normal_window_flags` — L185，46 行，控制流 5，Call 3
- `_apply_window_theme` — L257，27 行，控制流 5，Call 7
- `_prepare_window` — L286，56 行，控制流 12，Call 14
- `_show_and_activate` — L344，29 行，控制流 6，Call 6
## `core/animation_utils.py`

- `get_animation_curves` — L138，75 行，控制流 13，Call 6
- `reset_transform_channels` — L291，108 行，控制流 13，Call 18
- `normalize_nodes` — L446，34 行，控制流 5，Call 3
- `get_keyed_plugs` — L482，41 行，控制流 5，Call 4
- `get_key_data` — L543，57 行，控制流 3，Call 8
- `collect_animation` — L602，64 行，控制流 5，Call 6
- `validate_animation_data` — L743，46 行，控制流 4，Call 12
- `apply_attribute_keys` — L819，78 行，控制流 10，Call 10
- `import_animation` — L899，99 行，控制流 8，Call 14
## `core/attr_utils.py`

- `Attr.__init__` — L90，54 行，控制流 4，Call 7
- `Attr._get_plug` — L145，40 行，控制流 5，Call 9
- `Attr.set_attr_state` — L221，55 行，控制流 4，Call 10
- `Attr._build_add_attr_kwargs` — L320，40 行，控制流 8，Call 1
- `Attr.add_attr` — L402，109 行，控制流 5，Call 11
- `Attr.set_value` — L546，121 行，控制流 9，Call 14
- `Attr.add_message_attr` — L734，46 行，控制流 2，Call 7
- `Attr.connect_message` — L781，69 行，控制流 5，Call 12
- `Attr.set_attrs_limits` — L940，64 行，控制流 5，Call 15
- `Attr.get_attrs_limits` — L1005，53 行，控制流 4，Call 8
- `Attr.set_attr_value` — L1106，47 行，控制流 0，Call 1
- `Attr.get_string_info` — L1242，38 行，控制流 6，Call 8
## `core/blendshape_utils.py`

- `get_mesh_shape` — L109，38 行，控制流 5，Call 3
- `get_transform` — L149，37 行，控制流 5，Call 3
- `find_blendshape` — L192，40 行，控制流 6，Call 4
- `get_targets` — L306，64 行，控制流 5，Call 8
- `remove_target` — L404，81 行，控制流 8，Call 9
- `add_or_replace_target` — L487，109 行，控制流 9，Call 17
- `duplicate_all_targets` — L602，110 行，控制流 8，Call 19
- `invert_shapes` — L741，107 行，控制流 10，Call 23
## `core/connection_utils.py`

- `connect_plugs` — L149，48 行，控制流 3，Call 8
## `core/constraint_utils.py`

- `_normalize_nodes` — L51，36 行，控制流 5，Call 3
- `_normalize_search_types` — L89，40 行，控制流 5，Call 4
- `create_constraint` — L161，60 行，控制流 2，Call 5
- `create_pole_vector_constraint` — L223，45 行，控制流 2，Call 6
- `get_constraints` — L274，59 行，控制流 5，Call 4
## `core/control_shape_utils.py`

- `get_selected_curve_transforms` — L207，49 行，控制流 7，Call 6
- `get_shape_data` — L262，81 行，控制流 5，Call 11
- `_create_temp_curve` — L436，56 行，控制流 7，Call 11
- `apply_shape_data` — L494，88 行，控制流 6，Call 17
- `save_shape_data` — L610，45 行，控制流 2，Call 8
- `mirror_shape` — L871，47 行，控制流 4，Call 7
## `core/curve_utils.py`

- `get_curve_shape` — L121，58 行，控制流 5，Call 7
- `sample_curve_by_length` — L390，86 行，控制流 2，Call 9
- `get_closest_parameter` — L478，65 行，控制流 4，Call 10
- `parameter_to_length_percentage` — L545，48 行，控制流 3，Call 5
- `create_point_on_curve_attachment` — L641，138 行，控制流 2，Call 22
- `create_curve_from_nodes` — L823，65 行，控制流 5，Call 10
- `create_curve_from_selected_edges` — L890，53 行，控制流 3，Call 4
## `core/export_utils.py`

- `export_fbx` — L75，103 行，控制流 9，Call 17
## `core/file_utils.py`

- `normalize_extensions` — L137，45 行，控制流 7，Call 6
- `find_files` — L188，109 行，控制流 10，Call 19
- `write_json` — L343，52 行，控制流 3，Call 6
## `core/hierarchy_utils.py`

- `get_descendants` — L195，79 行，控制流 7，Call 10
- `parent` — L280，82 行，控制流 6，Call 11
- `ensure_group` — L368，91 行，控制流 8，Call 15
- `insert_parent_group` — L461，95 行，控制流 5，Call 17
## `core/joint_chain_utils.py`

- `get_joint_path` — L98，69 行，控制流 5，Call 9
- `create_joints_at_items` — L200，101 行，控制流 7，Call 14
- `create_joints_on_curve_cvs` — L344，114 行，控制流 8，Call 14
## `core/joint_utils.py`

- `Joint.__init__` — L102，45 行，控制流 4，Call 10
- `Joint.create` — L153，89 行，控制流 8，Call 14
- `Joint.create_at_object` — L244，47 行，控制流 1，Call 4
- `Joint.set_joint_orient` — L324，54 行，控制流 4，Call 7
- `Joint.set_label` — L575，64 行，控制流 2，Call 7
- `Joint.tag` — L640，65 行，控制流 5，Call 13
## `core/matrix_utils.py`

- `get_matrix` — L39，48 行，控制流 5，Call 9
- `create_parent_matrix_constraint` — L158，128 行，控制流 5，Call 23
- `remove_parent_matrix_constraint` — L288，59 行，控制流 8，Call 8
## `core/mesh_utils.py`

- `validate_model_transform` — L61，55 行，控制流 3，Call 8
- `delete_model` — L122，46 行，控制流 4，Call 6
- `duplicate_model` — L174，78 行，控制流 6，Call 10
## `core/model_check_utils.py`

- `get_mesh_shapes` — L143，75 行，控制流 11，Call 9
- `get_dag_nodes` — L496，44 行，控制流 6，Call 6
- `check_duplicate_names` — L542，55 行，控制流 6，Call 10
- `check_construction_history` — L603，50 行，控制流 6，Call 11
- `check_transformations` — L689，63 行，控制流 5，Call 16
- `check_locked_normals` — L758，80 行，控制流 9，Call 13
- `run_checks` — L844，72 行，控制流 8，Call 14
- `fix_issue` — L922，57 行，控制流 7，Call 9
## `core/rename_utils.py`

- `get_name_token` — L92，48 行，控制流 2，Call 7
- `get_objects_by_scope` — L204，58 行，控制流 8，Call 8
- `rename_node` — L268，40 行，控制流 5，Call 5
- `search_replace` — L403，63 行，控制流 6，Call 7
- `number_to_alpha` — L472，53 行，控制流 4，Call 8
- `get_number_string` — L527，56 行，控制流 5，Call 5
- `auto_number` — L590，67 行，控制流 5，Call 8
- `build_pattern_name` — L663，52 行，控制流 2，Call 6
## `core/scene_clean_utils.py`

- `has_rig_history` — L284，37 行，控制流 5，Call 3
- `delete_empty_groups` — L381，78 行，控制流 10，Call 13
- `delete_history` — L465，50 行，控制流 5，Call 7
- `freeze_transformations` — L521，58 行，控制流 6，Call 8
- `unlock_and_show_attributes` — L585，58 行，控制流 5，Call 6
- `delete_unknown_nodes` — L690，42 行，控制流 6，Call 8
- `run_cleanup` — L739，83 行，控制流 8，Call 6
## `core/scene_utils.py`

- `validate_node` — L131，56 行，控制流 4，Call 11
- `ensure_nodes_available` — L189，46 行，控制流 6，Call 6
- `create_node` — L278，60 行，控制流 3，Call 6
- `get_selected_nodes` — L381，56 行，控制流 6，Call 3
- `ensure_object_set` — L443，85 行，控制流 10，Call 15
- `reference_scene` — L743，66 行，控制流 3，Call 4
## `core/skin_utils.py`

- `find_skin_cluster` — L106，57 行，控制流 7，Call 5
- `copy_skin_weights` — L206，96 行，控制流 6，Call 17
- `export_skin_weights` — L327，75 行，控制流 1，Call 11
- `import_skin_weights` — L408，105 行，控制流 7，Call 27
## `core/snap_utils.py`

- `get_item_world_rotation` — L123，52 行，控制流 7，Call 8
- `snap_to_average` — L181，102 行，控制流 11，Call 12
## `core/surface_utils.py`

- `get_surface_shape` — L107，52 行，控制流 5，Call 7
- `move_curve_copy` — L204，57 行，控制流 3，Call 4
- `create_surface_from_curve` — L263，105 行，控制流 4，Call 11
- `create_follicle` — L374，134 行，控制流 3，Call 14
- `create_even_follicles` — L510，86 行，控制流 5，Call 8
## `core/transform_utils.py`

- `set_world_matrix` — L255，48 行，控制流 3，Call 6
- `move_relative` — L309，73 行，控制流 6，Call 8
## `systems/body/skirt/builder.py`

- `SkirtRigBuilder._delete_setup_nodes` — L163，44 行，控制流 8，Call 7
- `SkirtRigBuilder._create_curve_blueprints` — L233，69 行，控制流 1，Call 13
- `SkirtRigBuilder.create_setup` — L304，48 行，控制流 0，Call 8
- `SkirtRigBuilder.build` — L457，150 行，控制流 5，Call 23
## `systems/ctrl_base.py`

- `create_fk_ctrl` — L476，119 行，控制流 8，Call 11
- `create_follow` — L601，175 行，控制流 3，Call 28
- `create_space_switch` — L782，238 行，控制流 11，Call 48
- `_get_attr_definition` — L1026，85 行，控制流 10，Call 12
- `save_rebuild_cache` — L1190，129 行，控制流 7，Call 24
- `_create_cached_attr` — L1325，46 行，控制流 2，Call 4
- `_restore_cached_connections` — L1406，64 行，控制流 6，Call 13
- `restore_rebuild_cache` — L1472，143 行，控制流 11，Call 24
## `systems/face/build/curve_attachment.py`

- `attach_joints_to_curves` — L128，391 行，控制流 18，Call 56
## `systems/face/build/eyelid/builder.py`

- `build_radial_curve_joints` — L32，297 行，控制流 8，Call 42
## `systems/face/build/lip/zip_builder.py`

- `insert_zip_offset_group` — L37，59 行，控制流 1，Call 7
- `create_rest_world_matrix` — L98，83 行，控制流 1，Call 11
- `connect_world_matrix_to_transform` — L183，86 行，控制流 1，Call 12
- `create_zip_influence` — L319，140 行，控制流 2，Call 18
- `build_zip_pair` — L465，211 行，控制流 5，Call 30
- `build_zip_lip` — L683，288 行，控制流 20，Call 50
## `systems/face/face_base.py`

- `FaceBase.__init__` — L104，63 行，控制流 2，Call 3
- `FaceBase.ensure_config_layout` — L339，58 行，控制流 2，Call 9
- `FaceBase.validate_setup_config` — L614，61 行，控制流 6，Call 7
- `FaceBase.invalidate_later_steps` — L811，48 行，控制流 3，Call 5
## `systems/face/guide/face_guide.py`

- `FaceGuide.get_template_locator_names` — L245，54 行，控制流 6，Call 10
- `FaceGuide.get_imported_template_root` — L315，54 行，控制流 5，Call 8
- `FaceGuide.build_guide` — L419，112 行，控制流 11，Call 28
- `FaceGuide.set_world_matrix_preserve_lock` — L565，66 行，控制流 5，Call 8
- `FaceGuide.restore_guide_state` — L632，49 行，控制流 4，Call 7
- `FaceGuide.set_attr_preserve_lock` — L750，52 行，控制流 4，Call 6
- `FaceGuide.get_guide_node` — L845，82 行，控制流 10，Call 15
- `FaceGuide.get_guide_locators` — L928，40 行，控制流 5，Call 7
- `FaceGuide.get_part_guides` — L1002，74 行，控制流 8，Call 9
- `FaceGuide.get_lip_guides` — L1119，49 行，控制流 0，Call 19
- `FaceGuide.get_eyelid_guides` — L1169，62 行，控制流 1，Call 11
- `FaceGuide.get_eye_guides` — L1270，48 行，控制流 1，Call 5
- `FaceGuide.copy_attribute` — L1477，45 行，控制流 2，Call 7
- `FaceGuide.capture_side_state` — L1523，59 行，控制流 3，Call 9
- `FaceGuide.restore_mirror_snapshot` — L1621，76 行，控制流 6，Call 16
- `FaceGuide.mirror_zero_group` — L1698，74 行，控制流 5，Call 9
- `FaceGuide.apply_mirror` — L1815，89 行，控制流 3，Call 15
- `FaceGuide.validate_guides` — L1955，87 行，控制流 11，Call 16
- `FaceGuide.validate_controller_settings` — L2110，86 行，控制流 9，Call 20
## `systems/face/modules/teeth.py`

- `TeethModule.__init__` — L50，45 行，控制流 0，Call 3
- `TeethModule.collect_inputs` — L100，48 行，控制流 0，Call 9
- `TeethModule._prepare_names` — L234，46 行，控制流 0，Call 8
- `TeethModule._validate_build_nodes_available` — L311，44 行，控制流 5，Call 5
## `systems/face/naming.py`

- `create_role_name` — L34，48 行，控制流 1，Call 5
## `systems/face/setup/face_setup.py`

- `FaceSetup.__init__` — L42，51 行，控制流 0，Call 2
- `FaceSetup.collect_inputs` — L98，73 行，控制流 3，Call 10
## `systems/face/ui/build_controller.py`

- `FaceRigWizard.create_step2_page` — L64，94 行，控制流 1，Call 26
- `FaceRigWizard.load_step2_controller_settings` — L202，67 行，控制流 4，Call 16
- `FaceRigWizard.create_step3_page` — L293，145 行，控制流 0，Call 40
- `FaceRigWizard.clicked_build_teeth` — L457，59 行，控制流 1，Call 14
## `systems/face/ui/face_rig_ui.py`

- `FaceRigWizard.__init__` — L60，49 行，控制流 0，Call 12
- `FaceRigWizard.create_widgets` — L114，55 行，控制流 1，Call 15
- `FaceRigWizard.create_layouts` — L198，78 行，控制流 1，Call 19
- `FaceRigWizard.create_connections` — L277，48 行，控制流 3，Call 12
- `FaceRigWizard.create_step1_page` — L330，179 行，控制流 1，Call 47
- `FaceRigWizard.create_step2_page` — L514，344 行，控制流 2，Call 84
- `FaceRigWizard.create_placeholder_page` — L893，72 行，控制流 0，Call 15
- `FaceRigWizard.restore_step_state` — L993，59 行，控制流 5，Call 14
- `FaceRigWizard.build_step1` — L1246，46 行，控制流 1，Call 17
- `FaceRigWizard.enter_step2` — L1297，46 行，控制流 3，Call 13
- `FaceRigWizard.mirror_step2_guides` — L1484，54 行，控制流 1，Call 13
- `FaceRigWizard.load_step2_controller_settings` — L1604，53 行，控制流 3，Call 13
- `FaceRigWizard.finalize_step2` — L1713，70 行，控制流 3，Call 23
## `systems/face/ui/workflow_controller.py`

- `FaceRigWizard.create_layouts` — L68，100 行，控制流 1，Call 25
- `FaceRigWizard.reload_ui_from_scene` — L204，64 行，控制流 5，Call 14
- `FaceRigWizard.get_channel_box_config_attributes` — L310，46 行，控制流 3，Call 4
- `FaceRigWizard.set_channel_box_state` — L391，69 行，控制流 8，Call 9
- `FaceRigWizard.apply_config_channel_box_display` — L461，67 行，控制流 5，Call 10
- `FaceRigWizard.create_step2_page` — L533，77 行，控制流 7，Call 14
- `FaceRigWizard.load_step1_config_to_ui` — L678，56 行，控制流 4，Call 11
- `FaceRigWizard.load_step2_controller_settings` — L792，67 行，控制流 5，Call 15
- `FaceRigWizard.set_node_visibility` — L963，57 行，控制流 7，Call 8
- `FaceRigWizard.get_model_branch_under_root` — L1050，49 行，控制流 5，Call 3
- `FaceRigWizard.apply_setup_source_model_visibility` — L1100，77 行，控制流 11，Call 10
- `FaceRigWizard.apply_step_scene_visibility` — L1178，53 行，控制流 5，Call 6
## `systems/rig/ui/modular_rig_ui.py`

- `ModularRigWindow.create_layouts` — L484，144 行，控制流 1，Call 136
- `ModularRigWindow.create_connections` — L652，22 行，控制流 0，Call 18
- `ModularRigWindow.current_module_changed` — L954，35 行，控制流 5，Call 9
- `ModularRigWindow.restore_joint_display_settings` — L1090，46 行，控制流 4，Call 11
## `systems/rig_base.py`

- `RigBase.compose` — L93，52 行，控制流 6，Call 1
- `RigBase.get_next_index` — L260，75 行，控制流 5，Call 9
## `tools/__init__.py`

- `_read_tool_mode` — L117，57 行，控制流 10，Call 6
- `_discover_tools` — L249，75 行，控制流 9，Call 14
## `tools/basic/attr_tool.py`

- `move_selected_channel_box_attr` — L56，107 行，控制流 10，Call 27
- `AttrTool.create_widgets` — L192，86 行，控制流 0，Call 41
- `AttrTool.create_layouts` — L279，66 行，控制流 0，Call 56
- `AttrTool.clicked_attr_set_button` — L430，62 行，控制流 4，Call 20
## `tools/basic/connections_tool.py`

- `ConnectionsTool.create_widgets` — L212，58 行，控制流 0，Call 33
- `ConnectionsTool.create_layouts` — L271，81 行，控制流 0，Call 62
- `ConnectionsTool.connect_default_attrs` — L454，45 行，控制流 3，Call 11
- `ConnectionsTool.connect_custom_attrs` — L592，49 行，控制流 4，Call 11
- `ConnectionsTool.break_custom_attrs` — L642，43 行，控制流 5，Call 10
- `ConnectionsTool.copy_input_connections` — L686，58 行，控制流 6，Call 12
## `tools/basic/constraint_tool.py`

- `ConstraintTool.create_widgets` — L110，64 行，控制流 0，Call 29
- `ConstraintTool.create_layouts` — L175，63 行，控制流 0，Call 45
## `tools/basic/rename_tool.py`

- `RenameTool.create_widgets` — L96，65 行，控制流 0，Call 40
- `RenameTool.create_layouts` — L162，85 行，控制流 0，Call 73
## `tools/blendshape/add_blendshape_tool.py`

- `BlendShapeTargetTool.create_widgets` — L68，35 行，控制流 0，Call 19
- `BlendShapeTargetTool.create_layouts` — L104，46 行，控制流 0，Call 33
- `BlendShapeTargetTool.add_targets` — L240，43 行，控制流 6，Call 12
## `tools/blendshape/invert_shape_tool.py`

- `InvertShapeTool.create_layouts` — L94，30 行，控制流 0，Call 20
- `InvertShapeTool.pick_correctives` — L136，32 行，控制流 5，Call 8
## `tools/clean/hierarchy_cleaner.py`

- `HierarchyCleaner.create_widgets` — L66，49 行，控制流 0，Call 24
- `HierarchyCleaner.create_layouts` — L116，40 行，控制流 0，Call 28
- `HierarchyCleaner.format_result` — L209，64 行，控制流 7，Call 14
- `HierarchyCleaner.execute_cleanup` — L274，39 行，控制流 3，Call 19
## `tools/clean/model_checker.py`

- `ModelChecker.create_widgets` — L81，62 行，控制流 0，Call 33
- `ModelChecker.create_layouts` — L144，50 行，控制流 0，Call 37
- `ModelChecker.run_check` — L283，36 行，控制流 4，Call 19
- `ModelChecker.populate_table` — L320，36 行，控制流 2，Call 18
- `ModelChecker.select_issue_nodes` — L380，31 行，控制流 6，Call 6
## `tools/controller/control_shape_tool.py`

- `ShapeListWidget.__init__` — L137，23 行，控制流 0，Call 15
- `ShapeListWidget.refresh` — L199，55 行，控制流 7，Call 20
- `ShapeListWidget.upload_control` — L323，63 行，控制流 6，Call 14
- `ControlShapeTool.create_widgets` — L513，64 行，控制流 0，Call 28
- `ControlShapeTool.create_layouts` — L578，65 行，控制流 0，Call 47
- `ControlShapeTool.rotate_shapes` — L670，31 行，控制流 5，Call 7
## `tools/controller/create_ctrl_tool.py`

- `ControlCreatorDialog.create_widgets` — L153，132 行，控制流 1，Call 54
- `ControlCreatorDialog.create_layouts` — L286，93 行，控制流 0，Call 69
- `ControlCreatorDialog.refresh_shape_library` — L401，78 行，控制流 9，Call 28
- `ControlCreatorDialog.get_create_targets` — L550，58 行，控制流 8，Call 8
- `ControlCreatorDialog.get_control_name` — L626，77 行，控制流 5，Call 12
- `ControlCreatorDialog.create_controls` — L708，81 行，控制流 5，Call 22
## `tools/controller/create_fk_ctrl_tool.py`

- `create_fk_controls` — L68，51 行，控制流 2，Call 4
## `tools/face/face_select_key_tool.py`

- `_ensure_driver_attribute` — L120，58 行，控制流 3，Call 8
- `create_driven_key_setup` — L181，146 行，控制流 9，Call 15
- `FaceDrivenKeyTool.create_widgets` — L353，32 行，控制流 0，Call 16
- `FaceDrivenKeyTool.create_layouts` — L386，39 行，控制流 0，Call 27
- `FaceDrivenKeyTool.execute` — L460，54 行，控制流 4，Call 15
## `tools/joint/joint_resamp_tool.py`

- `JointResamplingTool.create_layouts` — L116，36 行，控制流 0，Call 25
- `resample_joint` — L251，150 行，控制流 17，Call 27
## `tools/joint/joint_tool.py`

- `JointTool.create_widgets` — L100，60 行，控制流 0，Call 37
- `JointTool.create_layouts` — L161，100 行，控制流 0，Call 81
- `JointTool.create_connections` — L262，33 行，控制流 0，Call 29
- `JointTool.set_axis_visibility` — L449，54 行，控制流 9，Call 8
- `JointTool.create_child_joints` — L547，60 行，控制流 5，Call 15
- `JointTool.create_joints_on_curves` — L647，49 行，控制流 5，Call 11
## `tools/rig/rig_tool.py`

- `get_pole_vector_position` — L77，93 行，控制流 2，Call 17
- `create_ik_rig` — L173，226 行，控制流 6，Call 39
- `RigTool.create_widgets` — L511，46 行，控制流 0，Call 21
- `RigTool.create_layouts` — L558，92 行，控制流 1，Call 46
- `RigTool.create_connections` — L651，19 行，控制流 0，Call 15
- `RigTool.reset_attributes` — L826，59 行，控制流 7，Call 8
- `RigTool.create_default_groups` — L926，55 行，控制流 4，Call 7
- `RigTool.add_zero_groups` — L984，65 行，控制流 7，Call 13
- `RigTool.select_children` — L1051，36 行，控制流 5，Call 5
- `RigTool.rename_duplicate_nodes` — L1160，45 行，控制流 5，Call 9
## `tools/rig/skirt_ctrl_tool.py`

- `SkirtRigDialog.create_widgets` — L69，31 行，控制流 0，Call 18
- `SkirtRigDialog.create_layouts` — L101，67 行，控制流 0，Call 49
## `tools/skin/skin_tool.py`

- `SkinTool.create_widgets` — L71，37 行，控制流 0，Call 20
- `SkinTool.create_layouts` — L109，61 行，控制流 0，Call 43
- `SkinTool.import_selected` — L332，35 行，控制流 5，Call 10
## `ui/theme.py`

- `_build_style_sheet` — L77，106 行，控制流 0，Call 0
## `ui/widgets/color_index_slider.py`

- `MayaIndexColorSlider.__init__` — L80，71 行，控制流 0，Call 21
- `MayaIndexColorSlider.style_widgets` — L156，63 行，控制流 0，Call 2
## `ui/widgets/object_picker.py`

- `MayaObjectPicker.__init__` — L48，48 行，控制流 1，Call 13
- `MayaObjectPicker.pick_from_selection` — L212，55 行，控制流 4，Call 9
## `ui/window_utils.py`

- `_show_and_activate` — L130，35 行，控制流 6，Call 7
- `show_window` — L182，68 行，控制流 4，Call 12
