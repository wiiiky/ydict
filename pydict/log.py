# encoding=utf-8


import sys


class LogLevel(object):

    """日志级别 """
    VERBOSE = 0
    DEBUG = 1
    ERROR = 2

    @staticmethod
    def to_string(level):
        if level == LogLevel.VERBOSE:
            return 'VERBOSE'
        elif level == LogLevel.DEBUG:
            return 'DEBUG'
        return 'ERROR'


log_info = {
    'level': LogLevel.DEBUG,
    'file': sys.stdout
}


def log(level, msg):
    """
    记录日志
    level是日志级别
    msg是日志内容
    """
    global log_info
    if level < log_info['level']:
        return
    msg = '[%s] %s\n' % (LogLevel.to_string(level), msg)
    log_info['file'].write(msg)


def debug(msg):
    log(LogLevel.DEBUG, msg)


def verbose(msg):
    log(LogLevel.VERBOSE, msg)


def error(msg):
    log(LogLevel.ERROR, msg)
