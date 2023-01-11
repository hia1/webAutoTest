# -- coding: utf-8 --
import os
from configparser import ConfigParser

from selenium.webdriver.common.by import By
from POM.Utils.times import dt_strftime


class ConfigManager():
    #项目目录
    BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    #页面对象目录
    ELEMENT_PATH=os.path.join(BASE_DIR,"BASE")

    #页面元素目录
    PAGEELEMENT_PATH=os.path.join(BASE_DIR,"page_element")

    #测试数据目录
    TESTDATA_PATH = os.path.join(BASE_DIR, 'testData')

    #报告文件
    REPORT_PATH=os.path.join(BASE_DIR,"results","reports")

    #driver
    DRIVER_PATH=os.path.join(BASE_DIR,"Utils","driver")

    #case
    CASE_PATH=os.path.join(BASE_DIR, "TestSuites",'cases')

    # 元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME
    }

    @property
    def allure_json(self):
        return os.path.join(cm.REPORT_PATH, 'allure_json')

    @property
    def allure_xml(self):
        return os.path.join(cm.REPORT_PATH, 'allure_xml')

    @property
    def pytest_html(self):
        return os.path.join(cm.REPORT_PATH, 'pytest_html')

    @property
    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'results', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime('%Y%m%d')))

    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" %ini_file)
        return ini_file


cm = ConfigManager()
if __name__ == '__main__':
    print(cm.BASE_DIR)
    log=cm.log_file
    print(log)
    print(cm.ini_file)
    # cf = ConfigParser()
    # cf.read(cm.ini_file)
    # print(cf.sections())

