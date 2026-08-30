# coding=utf-8
u"""
Architecture Cleanup Phase 2 Runner
===================================

给一次性 Phase 2 Migration 提供一个窄范围修正版入口。

原迁移脚本对 scene_utils.validate_node() 的 Args Docstring 使用全文件字符串匹配，
而相同 Docstring 片段在当前文件中出现两次。这里仅覆盖这一项迁移，
其它迁移步骤继续复用 architecture_cleanup_phase2.py，避免扩大修改面。
"""

from __future__ import print_function

from scripts import architecture_cleanup_phase2 as migration


def update_scene_utils():
    u"""稳定迁移 scene_utils.validate_node(node, label=None)。"""
    path = "core/scene_utils.py"
    source_text = migration.read_text(path)

    source_text = migration.replace_required(
        source_text,
        "def validate_node(node):\n",
        "def validate_node(node, label=None):\n",
        "scene_utils.validate_node signature"
    )

    # Args 章节不在这里做全文件字符串替换。
    # 后续 normalize_runtime_docstrings.py 会根据真实函数签名自动补齐 label 参数文档。
    source_text = migration.replace_required(
        source_text,
        "    # 步骤 1：空名称没有任何查询意义，直接报错。\n"
        "    if not node:\n"
        "        raise RuntimeError(u\"节点名称不能为空。\")\n\n"
        "    # 步骤 2：使用 objExists 检查 DAG / DG 节点。\n"
        "    if not cmds.objExists(node):\n"
        "        raise RuntimeError(\n"
        "            u\"Maya 节点不存在：{}\".format(node)\n"
        "        )\n",
        "    display_label = label or u\"Maya 节点\"\n\n"
        "    # 步骤 1：空名称没有任何查询意义，直接报错。\n"
        "    if not node:\n"
        "        raise RuntimeError(\n"
        "            u\"{}名称不能为空。\".format(\n"
        "                display_label\n"
        "            )\n"
        "        )\n\n"
        "    # 步骤 2：使用 objExists 检查 DAG / DG 节点。\n"
        "    if not cmds.objExists(node):\n"
        "        raise RuntimeError(\n"
        "            u\"{}不存在：{}\".format(\n"
        "                display_label,\n"
        "                node\n"
        "            )\n"
        "        )\n",
        "scene_utils.validate_node body"
    )

    migration.write_text(
        path,
        source_text
    )


def run():
    u"""运行带窄范围 Scene Migration 修复的 Phase 2 清理。"""
    migration.update_scene_utils = update_scene_utils
    migration.run()


if __name__ == "__main__":
    run()
