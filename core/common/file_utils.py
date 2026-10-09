# coding=utf-8
"""file_utils：供工具 UI 调用的 Maya 操作。"""

from __future__ import print_function
import json
import os

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
        当前 API 完成处理后返回的结果。

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
        当前 API 完成处理后返回的结果。

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
