# -- coding: utf-8 --

'''
每个页面继承BasePage,因为每个页面具有都有独有逻辑，解耦，便于代码维护
'''
from com.yang.practice100.POM.BASE.BasePage import BasePage


class GushiwenIndex(BasePage):
    #调用父类方法 打开
    INDEX_URL="https://www.gushiwen.cn/"

    def __init__(self, driver):
        super().__init__(driver)

    def open_index(self):
        self.get_url(self.INDEX_URL)

    def send_values(self,text,selector):
        self.sendKeys(text,selector)

    def click(self,selector):
        self.click_options(selector)

