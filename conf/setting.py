# coding=utf-8
"""
这是一个自定义设置的类
"""
from __future__ import unicode_literals,print_function

import os
import json
import codecs

import muziToolset.conf.config as config

# 获取设置文件的绝对路径

SETTING_FILE = os.path.join(config.PATH,"setting.json")

def _open_setting_file():
    """
    打开设置文件
    Returns:

    """
    if not os.path.isfile(SETTING_FILE):
        # codecs专门用作编码转换，codecs模块提供一个open方法，三个参数encoding, errors, buffering，
        # 这三个参数都是可选参数，但是对于应用来说，需要明确指定encoding的值，而errors和buffering使用默认值即可
        with codecs.open(SETTING_FILE, "w", encoding= "utf-8") as f:
            json.dump(dict(),f)

    else:
        with codecs.open(SETTING_FILE, "r", encoding = "utf-8") as f:
            return json.load(f)

def _save_setting_file(data):
    """
    保存设置文件
    Args:
        date: 保存设置文件的资料

    Returns:

    """
    with codecs.open(SETTING_FILE,"w",encoding = "utf-8") as f:
        json.dump(data,f)

def set(key,val):
    """
    设置属性和值
    Args:
        key: 属性
        val: 值

    Returns:

    """
    data = _open_setting_file()
    data[key] = val
    _save_setting_file(data)

def get(key,default):
    """
    获取属性和默认值
    Args:
        key: 属性
        default (object): 默认值

    Returns:

    """
    data = _open_setting_file()
    return data.get(key,default)