import logging
import os
import sys
import socket
import datetime
import platform
import time

dt = datetime.date.today().strftime('%Y-%m-%d')
ip = socket.gethostbyname((socket.gethostname()))

if platform.system() == 'Windows':
    # 文件和日志的主目录
    file_log_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1])+'/file_log'
    the_log_path = file_log_path + '/run_logs/windows_run_log.%s' % dt
elif ip == '172.16.6.75':
    # 文件和日志的主目录
    file_log_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])+'/file_log'
    the_log_path = file_log_path + '/run_logs/shengchan_run_log.%s' % dt
else:
    # 文件和日志的主目录
    file_log_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]) + '/file_log'
    the_log_path = file_log_path + '/run_logs/ceshi_run_log.%s' % dt

# 临时文件目录
tem_file_path = file_log_path + '/last_files'
# 临时文件名称
tem_file_name = tem_file_path + '/tem_file_%s-%s' % (sys.argv[0].split('/')[-1].split('.')[0], int(time.time()))


def get_logger(log_path=the_log_path, file_level='INFO', print_level='INFO', log_name='new_log'):
    log_dir = os.path.dirname(log_path)
    print('日志路径：'+log_path)
    if not os.path.exists(log_dir):
        raise Exception("'%s' 文件夹路径不存在，请先创建路径" % log_dir)
    f_level = file_level.lower()
    p_level = print_level.lower()
    dic_level = {'debug': logging.DEBUG, 'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR,
                 'critical': logging.CRITICAL}
    for tem in [f_level, p_level]:
        if tem not in dic_level:
            raise Exception("日志等级或打印等级不符合条件")
    # 实例化一个名为new_log的logger
    logger = logging.getLogger(log_name)
    # 初始化默认所有级别日志都可以被写入和打印到控制台
    logger.setLevel(dic_level[f_level])
    # 创建日志写入文件工具fh，并把fh添加到logger
    fh = logging.FileHandler(log_path)
    fh.setLevel(dic_level[p_level])  # 设置写入文件的日志的级别
    formatter = logging.Formatter("%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s")
    fh.setFormatter(formatter)  # 设置日志写入文件格式为formatter
    # 添加日志打印到控制台工具sh，并把sh添加到logger
    sh = logging.StreamHandler()  # 实例化sh
    sh.setLevel(print_level)   # 设置打印到控制台的日志级别
    formatter = logging.Formatter("%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s")
    sh.setFormatter(formatter)  # 设置打印日志格式
    if not logger.handlers:
        logger.addHandler(fh)  # fh添加到logger
        logger.addHandler(sh)  # sh添加到logger
    return logger


if __name__ == '__main__':
    logger1 = get_logger()
    logger2 = get_logger()
    logger3 = get_logger()
    logger1.info('abc')
    logger2.error('def')
    logger3.warning('ghi')
