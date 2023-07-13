#日志的使用
import logging
#设置日志的提示级别信息，以及保存日志的名称(可以采用绝对路径，如果只给名字的话，日志生成的文件会在当前文件夹下)，保存日志的方式
logging.basicConfig(level = logging.DEBUG,filename = 'app.log',filemode = 'a')

#日志提示的不同级别
logging.debug(1)
logging.info(2)
logging.warning(3)
logging.error(4)
logging.critical(5)