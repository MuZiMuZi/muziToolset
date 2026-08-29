# coding=utf-8
u"""
File Utils
==========

通用文件和 JSON 底层工具。

职责：
    1. 规范化文件路径；
    2. 创建目录；
    3. 读取 / 写入 JSON。

本模块不依赖 Maya UI，不弹出 QFileDialog，也不负责打开 Maya Scene。
"""

from __future__ import print_function

import json
import os


def normalize_path(file_path):
    """返回统一使用正斜杠的规范路径。"""
    if not file_path:
        return ""

    normalized_path = os.path.normpath(file_path)
    normalized_path = normalized_path.replace("\\", "/")
    return normalized_path


def ensure_directory(directory):
    """确保目录存在，并返回规范后的目录路径。"""
    if not directory:
        raise ValueError(u"directory 不能为空。")

    normalized_directory = normalize_path(directory)

    if not os.path.isdir(normalized_directory):
        os.makedirs(normalized_directory)

    return normalized_directory


def read_json(file_path, default=None):
    """读取 UTF-8 JSON 文件。"""
    normalized_path = normalize_path(file_path)

    if not normalized_path:
        raise ValueError(u"file_path 不能为空。")

    if not os.path.isfile(normalized_path):
        if default is not None:
            return default

        raise RuntimeError(
            u"JSON 文件不存在：{}".format(normalized_path)
        )

    with open(normalized_path, "r") as file_object:
        return json.load(file_object)


def write_json(
        file_path,
        data,
        indent=4,
        ensure_ascii=False,
        sort_keys=False
):
    """把数据写入 UTF-8 JSON 文件，并自动创建父目录。"""
    normalized_path = normalize_path(file_path)

    if not normalized_path:
        raise ValueError(u"file_path 不能为空。")

    parent_directory = os.path.dirname(normalized_path)

    if parent_directory:
        ensure_directory(parent_directory)

    with open(normalized_path, "w") as file_object:
        json.dump(
            data,
            file_object,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=sort_keys
        )

    return normalized_path


def get_file_name(file_path):
    """返回路径中的文件名。"""
    normalized_path = normalize_path(file_path)
    return os.path.basename(normalized_path)


def get_file_stem(file_path):
    """返回不包含扩展名的文件名。"""
    file_name = get_file_name(file_path)
    stem, extension = os.path.splitext(file_name)
    return stem


__all__ = [
    "normalize_path",
    "ensure_directory",
    "read_json",
    "write_json",
    "get_file_name",
    "get_file_stem",
]
