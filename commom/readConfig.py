# -- coding: utf-8 --
'''用于读取解析config下面的配置文件'''
import configparser
from typing import Type
from POM.config.config import cm
from configparser import ConfigParser

WEB_INFO = 'web_info'
LOGLEVEL = 'loglevel'
FIREFOX_BIN = 'firefox_binary'
TESTCASE = 'testcase'
CONTROLLER_INFO = 'controller_info'

class ReadConfig():
    def __init__(self):
        self.configParser=ConfigParser()
        self.configParser.read(cm.ini_file,encoding="utf-8")

    #读取配置文件
    def _get(self,section,option):
        return self.configParser.get(section,option)


    #更新配置文件
    def _set(self,section,option,value):
        self.configParser.set(section,option,value)
        with open(cm.ini_file,"w") as fp:
            self.configParser.write(fp)

    '''取指定配置数据的方法'''
    #property-装饰器 修饰方法：使方法可以像属性一样使用，只读属性，防止修改
    @property
    def web_url(self):
        return self._get(WEB_INFO, 'web_info')
    @property
    def web_username(self):
        return self._get(WEB_INFO, 'web_username')
    @property
    def web_passward(self):
        return self._get(WEB_INFO, 'web_passward')

    @property
    def loglevel(self):
        return self._get(LOGLEVEL, LOGLEVEL).upper()

    @property
    def firefox_binary(self):
        return self._get(FIREFOX_BIN,FIREFOX_BIN)

    @property
    def web_broswer(self):
        return self._get(WEB_INFO,"web_broswer")

    @property
    def testcase(self):
        return self._get(TESTCASE, TESTCASE).split(',')

    @property
    def test_case(self):
        '''返回测试步骤excel文件路径'''
        return self._get(TESTCASE,"testcase_excel")


    @property
    def controller_host(self):
        return self._get(CONTROLLER_INFO, 'controller_host')

    @property
    def controller_pwd(self):
        return self._get(CONTROLLER_INFO, 'controller_pwd')

conf=ReadConfig()

if __name__ == '__main__':
    print(conf.web_url)
    print(conf.loglevel)
    print(conf.test_case)