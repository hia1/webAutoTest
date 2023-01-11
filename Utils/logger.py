# -- coding: utf-8 --
import logging

from POM.commom.readConfig import conf
from POM.config.config import cm

class Log():
    def __init__(self) -> None:
        self.logger=logging.getLogger()
        self.logger.setLevel(conf.loglevel)
        if self.logger.handlers:
            self.logger.handlers.clear()

        #创建一个handle写入文件
        fh=logging.FileHandler(cm.log_file,encoding="utf-8")
        fh.setLevel(conf.loglevel)

        #创建一个handle输出控制台
        sh=logging.StreamHandler()
        sh.setLevel(conf.loglevel)

        #定义输出格式
        formatter = logging.Formatter(self.fmt)
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        #添加到handle
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    @property
    def fmt(self):
        return  '%(levelname)s\t%(asctime)s\t[%(filename)s:%(lineno)d]\t%(message)s'


log=Log().logger
if __name__ == '__main__':

    log.debug("hell world")