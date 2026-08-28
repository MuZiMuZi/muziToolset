# 日志的使用
import logging

#设置自定义的logger模块，这样在项目里有多个文件的时候可以定义是哪个文件传出的日志信息，方便排查错误
logger = logging.getLogger('my_custom_logger')


# level：设置日志的提示级别信息，
# filename：保存日志的名称(可以采用绝对路径，如果只给名字的话，日志生成的文件会在当前文件夹下)
# filemode：保存日志的方式
# format：设置保存日志的信息
# datefmt：设置保存日志的时间（asctime）的格式
logging.basicConfig(level = logging.DEBUG , filename = 'app.log' , filemode = 'a' ,
                    format = '%(asctime)s -%(name)s - %(levelname)s - %(message)s' ,
                    datefmt = '%d - %b - %y %H:%M:%S')

# 日志提示的不同级别
logger.debug(1)
logger.info(2)
logger.warning(3)
logger.error(4)
logger.critical(5)

#将报错信息记录起来
try:
    1/0
except Exception as e:
    logger.error(e,exc_info = True)