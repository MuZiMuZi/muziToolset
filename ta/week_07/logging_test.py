# coding=utf-8

import logging


# 设置自定义logging名称
logger = logging.getLogger('my_custom_logger')


# 设置打印的日志级别,注意INFO需要大写，这是一个变量
# filename 表示需要存储日志的文件路径，可以使用绝对路径。
# filemode表示存储日志的方式，=‘a’表示会在日志文件的末尾新添加日志
# format表示书写的格式
# asctime表示程序运行到这一步的时间
# levelname表示日志的级别
# message表示日志级别设置的信息
logging.basicConfig(level = logging.DEBUG, filename = 'app.log', filemode = 'a',
                    format = '%(asctime)s  - %(name)s  - %(levelname)s  - %(message)s')

# 日志级别
logger.debug(1)  # 开发过程中debug
logger.info(2)  # 记录需要的信息
logger.warning(3)  # 警告提示
logger.error(4)  # 错误提示
logger.critical(5)  # 程序崩溃或严重的错误提示


# 设置详细的报错信息
try:
    1/0
except Exception as e :
    logger.error(e,exc_info = True)