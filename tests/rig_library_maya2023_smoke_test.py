# coding=utf-8
u"""Maya 2023 绑定库运行测试。仅在新的空场景中显式运行，保留结果供目视检查。"""


def run():
    u"""验证 Face Starter、Locator 可见位置、幂等构建和控制器外观。"""
    import maya.cmds as cmds
    from ..systems.rig.library_service import RigLibraryService
    from ..systems.rig import library_catalog as catalog

    # 拒绝占用用户已有场景，不执行 file(new=True, force=True)。
    if cmds.file(query=True, sceneName=True):
        raise RuntimeError(u"请先新建一个空场景，再运行绑定库测试。")
    for node in cmds.ls(assemblies=True) or []:
        if node not in ("persp", "top", "front", "side"):
            raise RuntimeError(u"场景不是空场景，请先保存当前工作并新建场景。")
    service = RigLibraryService()
    if service.document["modules"]:
        raise RuntimeError(u"当前场景已有绑定库配置，请使用新的空场景。")
    service.add_template("face_starter")
    service.setup()
    service.import_guide()
    errors = service.validate()
    if errors:
        raise RuntimeError("\n".join(errors))
    assert service.build() == 3
    controls = []
    joints = []
    before_matrices = {}
    before_connections = {}
    positions_checked = 0
    for record in service.document["modules"]:
        outputs = catalog.output_names(record)
        guides = catalog.guide_names(record)
        for index, guide in enumerate(guides):
            shapes = cmds.listRelatives(guide, shapes=True, type="locator", fullPath=True) or []
            expected = cmds.getAttr(shapes[0] + ".worldPosition[0]")[0]
            for node in (outputs["joints"][index], outputs["controls"][index]):
                position = cmds.xform(node, query=True, worldSpace=True, translation=True)
                for axis in range(3):
                    assert abs(position[axis] - expected[axis]) < 0.0001, (node, position, expected)
            positions_checked += 1
        controls.extend(outputs["controls"])
        joints.extend(outputs["joints"])
        for node in outputs["joints"] + outputs["controls"] + outputs["outputs"]:
            before_matrices[node] = cmds.xform(node, query=True, worldSpace=True, matrix=True)
            before_connections[node] = sorted(cmds.listConnections(node, connections=True, plugs=True) or [])

    assert len(controls) == 11
    assert len(joints) == 11
    before_nodes = set(cmds.ls(long=True))
    assert service.build() == 0
    assert before_nodes == set(cmds.ls(long=True))

    record = service.document["modules"][0]
    output = catalog.output_names(record)
    shape = cmds.listRelatives(output["controls"][0], shapes=True, type="nurbsCurve", fullPath=True)[0]
    before_points = cmds.xform(shape + ".cv[*]", query=True, objectSpace=True, translation=True)
    service.update_module(record["id"], {"ctrl_size": 2.0, "ctrl_color": 18, "ctrl_axis": "Z+"})
    service.update_module(record["id"], {"ctrl_size": 1.0, "ctrl_color": 6, "ctrl_axis": "X+"})
    after_points = cmds.xform(shape + ".cv[*]", query=True, objectSpace=True, translation=True)
    for index in range(len(before_points)):
        assert abs(before_points[index] - after_points[index]) < 0.0001
    for node in before_matrices:
        after_matrix = cmds.xform(node, query=True, worldSpace=True, matrix=True)
        for index in range(16):
            assert abs(before_matrices[node][index] - after_matrix[index]) < 0.0001, node
        assert before_connections[node] == sorted(cmds.listConnections(node, connections=True, plugs=True) or [])
    assert RigLibraryService().document == service.document
    result = {"passed": True, "modules": 3, "joints": len(joints),
              "controls": len(controls), "guide_positions_checked": positions_checked,
              "repeat_build": "skipped", "appearance_round_trip": "passed"}
    print(result)
    return result
