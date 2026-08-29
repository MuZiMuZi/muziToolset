# coding=utf-8
u"""
File Utils
==========

通用文件和 JSON 底层工具。

职责：
    1. 规范化文件路径；
    2. 创建目录；
    3. 读取 / 写入 JSON；
    4. 按扩展名扫描目录文件。

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


def normalize_extensions(extensions):
    """把扩展名统一成小写且带点号的列表。"""
    if extensions is None:
        return None

    if isinstance(extensions, str):
        extensions = [extensions]

    normalized_extensions = []

    for extension in extensions:
        if extension is None:
            continue

        extension = str(extension).strip().lower()

        if not extension:
            continue

        if not extension.startswith("."):
            extension = "." + extension

        if extension not in normalized_extensions:
            normalized_extensions.append(extension)

    return normalized_extensions


def find_files(
        directory,
        extensions=None,
        recursive=True,
        return_paths=True
):
    """
    按扩展名扫描目录文件。

    Args:
        directory(str): 根目录。
        extensions(str/list/None):
            例如 "ma"、["ma", "mb"] 或 [".json"]；None 表示全部文件。
        recursive(bool): 是否扫描子目录。
        return_paths(bool): True 返回完整路径，False 只返回文件名。

    Returns:
        list(str): 排序后的文件列表。
    """
    normalized_directory = normalize_path(directory)

    if not normalized_directory:
        raise ValueError(u"directory 不能为空。")

    if not os.path.isdir(normalized_directory):
        raise RuntimeError(
            u"目录不存在：{}".format(normalized_directory)
        )

    normalized_extensions = normalize_extensions(extensions)
    result = []

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

    if recursive:
        for root_directory, folder_names, file_names in os.walk(
                normalized_directory
        ):
            for file_name in file_names:
                append_file(
                    root_directory,
                    file_name
                )
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

    result.sort()
    return result


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
    "normalize_extensions",
    "find_files",
    "read_json",
    "write_json",
    "get_file_name",
    "get_file_stem",
]
