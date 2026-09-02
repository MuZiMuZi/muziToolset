# coding=utf-8
u"""
File Utils
==========

纯 Python 文件系统与 JSON 底层工具。

模块职责
--------
这个模块只处理“硬盘文件”和“路径”，不处理 Maya Scene 生命周期。
它可以被 Maya Tool 使用，也可以在普通 Python 环境中复用。

当前公开方法
------------
路径：
    normalize_path(file_path)
        规范化路径，并统一使用正斜杠。

    ensure_directory(directory)
        确保目录存在；不存在时自动创建。

扩展名 / 文件扫描：
    normalize_extensions(extensions)
        将扩展名统一成小写、带点号且去重的列表。

    find_files(directory, extensions=None, recursive=True, return_paths=True)
        按扩展名扫描目录，可选择递归和是否返回完整路径。

JSON：
    read_json(file_path, default=None)
        读取 UTF-8 JSON；文件不存在时可返回 default。

    write_json(file_path, data, indent=4, ensure_ascii=False, sort_keys=False)
        写入 UTF-8 JSON，并自动创建父目录。

文件名：
    get_file_name(file_path)
        取得路径中的完整文件名。

    get_file_stem(file_path)
        取得不带扩展名的文件名。

模块边界
--------
    硬盘路径 / JSON / 目录扫描   -> file_utils
    Maya Scene Open / Import     -> scene_utils
    动画 JSON 的业务结构        -> animation_utils

本模块不负责
------------
- Maya cmds.file；
- QFileDialog；
- Reference；
- FBX Export；
- Animation 数据结构定义。

设计原则
--------
1. 尽量保持纯 Python，不依赖 Maya；
2. 所有对外路径统一经过 normalize_path；
3. 写文件前自动创建父目录；
4. JSON 默认 UTF-8，中文内容不强制转成 Unicode Escape；
5. 文件扫描结果排序，保证同样目录得到稳定结果。
"""

from __future__ import print_function

import json
import os


# =============================================================================
# Path - 路径规范化与目录创建
# =============================================================================

def normalize_path(file_path):
    u"""
    返回统一使用正斜杠的规范路径。

    Args:
        file_path (str):
            输入路径。

    Returns:
        str: 规范化路径；空输入返回空字符串。
    """
    # 步骤 1：空路径直接返回空字符串，方便上层统一判断。
    if not file_path:
        return ""

    # 步骤 2：先让 os.path.normpath 处理多余分隔符和 .. / .。
    normalized_path = os.path.normpath(file_path)

    # 步骤 3：统一改成正斜杠。
    # Maya / JSON / 日志中使用正斜杠更稳定，也方便跨平台比较字符串。
    normalized_path = normalized_path.replace("\\", "/")

    return normalized_path


def ensure_directory(directory):
    u"""
    确保目录存在，并返回规范后的目录路径。

    目录不存在时会递归创建。

    Args:
        directory (str):
            需要读取或写入的目录路径。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：目录参数不能为空。
    if not directory:
        raise ValueError(u"directory 不能为空。")

    # 步骤 2：统一路径格式。
    normalized_directory = normalize_path(directory)

    # 步骤 3：目录不存在时创建。
    if not os.path.isdir(normalized_directory):
        os.makedirs(normalized_directory)

    return normalized_directory


# =============================================================================
# Extension - 扩展名整理
# =============================================================================

def normalize_extensions(extensions):
    u"""
    将扩展名统一成小写、带点号、保持顺序去重的列表。

    Args:
        extensions (str | list[str] | None):
            允许匹配的文件扩展名，例如 `.ma`、`.mb`、`.json`。

    Returns:
        object | None:
        方法执行后的结果数据。

    Example:
        ["MA", ".mb", "json"]
                                                                            -> [".ma", ".mb", ".json"]
    """
    # 步骤 1：None 表示不过滤扩展名。
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if extensions is None:
        return None

    # 步骤 2：单个字符串统一转成 list。
    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if isinstance(extensions, str):
        extensions = [extensions]

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    normalized_extensions = []

    # 步骤 3：逐个清洗扩展名。
    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for extension in extensions:
        if extension is None:
            continue

        extension = str(extension).strip().lower()

        if not extension:
            continue

        # 没有点号时自动补上。
        if not extension.startswith("."):
            extension = "." + extension

        # 保持原顺序去重。
        if extension not in normalized_extensions:
            normalized_extensions.append(extension)

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return normalized_extensions


# =============================================================================
# File Scan - 目录文件扫描
# =============================================================================

def find_files(
        directory,
        extensions=None,
        recursive=True,
        return_paths=True
):
    u"""
    按扩展名扫描目录文件。

    Args:
        directory (str):
            根目录。
        extensions (str/list/None):
            例如 "ma"、["ma", "mb"]、[".json"]； None 表示不过滤扩展名。
        recursive (bool):
            是否递归扫描子目录。
        return_paths (bool):
            True 返回完整路径； False 只返回文件名。

    Returns:
        list: 排序后的文件列表。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：规范化并验证根目录。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    normalized_directory = normalize_path(directory)

    if not normalized_directory:
        raise ValueError(u"directory 不能为空。")

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not os.path.isdir(normalized_directory):
        raise RuntimeError(
            u"目录不存在：{}".format(normalized_directory)
        )

    # -------------------------------------------------------------------------
    # 步骤 2：整理扩展名过滤条件。
    # -------------------------------------------------------------------------
    normalized_extensions = normalize_extensions(extensions)
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    result = []

    # -------------------------------------------------------------------------
    # 内部 Helper：判断文件扩展名，并按 return_paths 决定返回内容。
    # -------------------------------------------------------------------------
    def append_file(root_directory, file_name):
        extension = os.path.splitext(file_name)[1].lower()

        if normalized_extensions is not None:
            if extension not in normalized_extensions:
                return

        if return_paths:
            file_path = os.path.join(
                root_directory,
                file_name
            )
            result.append(
                normalize_path(file_path)
            )
        else:
            result.append(file_name)

    # -------------------------------------------------------------------------
    # 步骤 3：递归扫描模式。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if recursive:
        for root_directory, folder_names, file_names in os.walk(
                normalized_directory
        ):
            # folder_names 当前不需要修改，但保留变量名称让 os.walk 结构清晰。
            for file_name in file_names:
                append_file(
                    root_directory,
                    file_name
                )

    # -------------------------------------------------------------------------
    # 步骤 4：只扫描当前目录模式。
    # -------------------------------------------------------------------------
    else:
        item_names = os.listdir(
            normalized_directory
        )

        for item_name in item_names:
            item_path = os.path.join(
                normalized_directory,
                item_name
            )

            if not os.path.isfile(item_path):
                continue

            append_file(
                normalized_directory,
                item_name
            )

    # -------------------------------------------------------------------------
    # 步骤 5：排序后返回，保证结果稳定。
    # -------------------------------------------------------------------------
    result.sort()
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result


# =============================================================================
# JSON - 数据读写
# =============================================================================

def read_json(file_path, default=None):
    u"""
    读取 UTF-8 JSON 文件。

    Args:
        file_path (str):
            JSON 文件路径。
        default (any):
            文件不存在时可返回的默认值； default=None 时文件不存在会抛 RuntimeError。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：规范化路径。
    normalized_path = normalize_path(file_path)

    if not normalized_path:
        raise ValueError(u"file_path 不能为空。")

    # 步骤 2：处理文件不存在的情况。
    if not os.path.isfile(normalized_path):
        if default is not None:
            return default

        raise RuntimeError(
            u"JSON 文件不存在：{}".format(normalized_path)
        )

    # 步骤 3：读取并解析 JSON。
    with open(normalized_path, "r") as file_object:
        return json.load(file_object)


def write_json(
        file_path,
        data,
        indent=4,
        ensure_ascii=False,
        sort_keys=False
):
    u"""
    将数据写入 UTF-8 JSON 文件，并自动创建父目录。

    Args:
        file_path (str):
            需要读取或写入的文件路径。
        data (dict | list | object):
            需要序列化、恢复或传递的结构化数据。
        indent (int):
            写入 JSON 时使用的缩进空格数；None 表示紧凑输出。
        ensure_ascii (bool):
            写 JSON 时是否把非 ASCII 字符转义。
        sort_keys (bool):
            写 JSON 时是否按 Key 排序，便于版本控制 Diff。

    Returns:
        str: 最终写入路径。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：规范化输出路径。
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    normalized_path = normalize_path(file_path)

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not normalized_path:
        raise ValueError(u"file_path 不能为空。")

    # 步骤 2：确保父目录存在。
    parent_directory = os.path.dirname(normalized_path)

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if parent_directory:
        ensure_directory(parent_directory)

    # 步骤 3：写入 JSON。
    # -------------------------------------------------------------------------
    # Step 04：在受控上下文中执行当前阶段操作
    # -------------------------------------------------------------------------
    with open(normalized_path, "w") as file_object:
        json.dump(
            data,
            file_object,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=sort_keys
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return normalized_path


# =============================================================================
# File Name - 文件名拆分
# =============================================================================

def get_file_name(file_path):
    u"""
    返回路径中的完整文件名，例如 ``character.ma``。

    Args:
        file_path (str):
            需要读取或写入的文件路径。

    Returns:
        object:
        方法执行后的结果数据。
    """
    normalized_path = normalize_path(file_path)
    return os.path.basename(normalized_path)


def get_file_stem(file_path):
    u"""
    返回不包含扩展名的文件名，例如 ``character``。

    Args:
        file_path (str):
            需要读取或写入的文件路径。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 步骤 1：先取得文件名。
    file_name = get_file_name(file_path)

    # 步骤 2：拆分 Stem / Extension。
    stem, extension = os.path.splitext(file_name)

    return stem


__all__ = [
    "normalize_path",
    "ensure_directory",
    "normalize_extensions",
    "find_files",
    "read_json",
    "write_json",
    "get_file_name",
    "get_file_stem",
]
