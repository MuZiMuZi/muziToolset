# coding=utf-8
u"""一次性迁移 Face Module 最终生命周期命名，并在完成后自清理。"""

from __future__ import print_function

import os


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


def replace_text(file_path, replacements):
    u"""按明确映射替换文件内容；缺少预期文本时直接失败。"""
    absolute_path = os.path.join(
        REPO_ROOT,
        file_path
    )

    with open(absolute_path, "r", encoding="utf-8") as file_object:
        content = file_object.read()

    for old_text, new_text in replacements:
        if old_text not in content:
            raise RuntimeError(
                u"迁移目标不存在：{} | {}".format(
                    file_path,
                    old_text
                )
            )

        content = content.replace(
            old_text,
            new_text
        )

    with open(absolute_path, "w", encoding="utf-8", newline="\n") as file_object:
        file_object.write(
            content
        )


def migrate_module(file_path, module_name):
    u"""把具体 Face Module 迁到最终生命周期方法名。"""
    replacements = [
        ("def setup(self):", "def load_setup(self):"),
        ("def guide(self):", "def load_guide(self):"),
        ("def joint(self):", "def create_jnt(self):"),
        ("def control(self):", "def create_ctrl(self):"),
        ("def connect(self):", "def create_connect(self):"),
        ("def deform(self):", "def create_deform(self):"),
        ("def finalize(self):", "def create_finalize(self):"),
        ("{}Module.build()".format(module_name), "{}Module.create_build()".format(module_name)),
    ]

    replace_text(
        file_path,
        replacements
    )


def migrate_build_entry(file_path, variable_name):
    u"""把模块包装函数改为调用 create_build()。"""
    replace_text(
        file_path,
        [
            (
                "{}_dict = {}.build()".format(variable_name, variable_name),
                "{}_dict = {}.create_build()".format(variable_name, variable_name)
            ),
        ]
    )


def migrate_contract():
    u"""把 Face Module 生命周期静态 Contract 更新为最终 API。"""
    contract_path = os.path.join(
        REPO_ROOT,
        "tests",
        "face_module_lifecycle_contract_test.py"
    )

    with open(contract_path, "r", encoding="utf-8") as file_object:
        content = file_object.read()

    old_methods = '''FACE_MODULE_METHODS = [
    "setup",
    "guide",
    "joint",
    "control",
    "connect",
    "deform",
    "finalize",
]'''

    new_methods = '''FACE_MODULE_METHODS = [
    "load_setup",
    "load_guide",
    "create_jnt",
    "create_ctrl",
    "create_connect",
    "create_deform",
    "create_finalize",
]'''

    if old_methods not in content:
        raise RuntimeError(
            u"Face Module Contract 的旧生命周期列表不存在。"
        )

    content = content.replace(
        old_methods,
        new_methods
    )

    old_retired = '''RETIRED_CONCRETE_METHODS = {
    "collect_inputs",
    "prepare_data",
    "process_data",
    "finalize_step",
    "create_joint",
    "create_controller",
    "create_connection",
}'''

    new_retired = '''RETIRED_CONCRETE_METHODS = {
    "collect_inputs",
    "prepare_data",
    "process_data",
    "finalize_step",
    "create_joint",
    "create_controller",
    "create_connection",
    "setup",
    "guide",
    "joint",
    "control",
    "connect",
    "deform",
    "finalize",
    "build",
}'''

    if old_retired not in content:
        raise RuntimeError(
            u"Face Module Contract 的旧废弃方法列表不存在。"
        )

    content = content.replace(
        old_retired,
        new_retired
    )
    content = content.replace(
        "2. build() 的执行顺序固定；",
        "2. create_build() 的执行顺序固定；"
    )
    content = content.replace(
        "5. build_xxx() 公共入口统一调用 module.build()。",
        "5. build_xxx() 公共入口统一调用 module.create_build()。"
    )
    content = content.replace(
        'required_methods.append(\n        "build"\n    )',
        'required_methods.append(\n        "create_build"\n    )'
    )
    content = content.replace(
        'if node.name == "build":',
        'if node.name == "create_build":'
    )
    content = content.replace(
        u"FaceModuleBase 缺少 build()。",
        u"FaceModuleBase 缺少 create_build()。"
    )
    content = content.replace(
        u"FaceModuleBase.build() 生命周期顺序错误：{}",
        u"FaceModuleBase.create_build() 生命周期顺序错误：{}"
    )
    content = content.replace(
        u"验证 FaceModuleBase 的生命周期方法和 build() 顺序。",
        u"验证 FaceModuleBase 的生命周期方法和 create_build() 顺序。"
    )

    with open(contract_path, "w", encoding="utf-8", newline="\n") as file_object:
        file_object.write(
            content
        )


def cleanup_temporary_files():
    u"""删除本次迁移使用的一次性脚本与 Workflow。"""
    temporary_paths = [
        os.path.join(
            REPO_ROOT,
            ".github",
            "workflows",
            "migrate_face_module_naming.yml"
        ),
        os.path.abspath(__file__),
    ]

    for temporary_path in temporary_paths:
        if not os.path.exists(temporary_path):
            continue

        os.remove(
            temporary_path
        )


def main():
    u"""执行最终 Face Module 生命周期命名迁移。"""
    migrate_module(
        "systems/face/modules/jaw.py",
        "Jaw"
    )
    migrate_build_entry(
        "systems/face/modules/jaw.py",
        "jaw_module"
    )

    migrate_module(
        "systems/face/modules/teeth.py",
        "Teeth"
    )
    migrate_build_entry(
        "systems/face/modules/teeth.py",
        "teeth_module"
    )

    migrate_contract()
    cleanup_temporary_files()

    print(
        u"Face Module 最终生命周期命名迁移完成。"
    )


if __name__ == "__main__":
    main()
