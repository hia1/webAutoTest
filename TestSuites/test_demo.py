# -- coding: utf-8 --
import sys
import time
import pytest
import pytest_rerunfailures
from selenium import webdriver

from practice100.POM.BASE.BasePage import BasePage, base
from practice100.POM.Utils.utils import SeleniumAdapter
from practice100.POM.commom.readConfig import conf
from pytest_selenium import selenium

class TestClass():
    flag = True
    driver_inst= webdriver.Chrome()
    basePage = BasePage(driver_inst)
    url=conf.web_url
    selenium(driver_inst)

    def setup_class(self):
        print("执行测试类前开始执行"+'*'*8)
        self.basePage.get_url(self.url)
        print("执行测试类前完成执行"+'*'*8)

    def teardown_class(self):
        print("执行测试类后开始执行" + '*' * 8)
        self.basePage.quit_browser()
        print("执行测试类后完成执行" + '*' * 8)



    def setup_method(self):
        print("every case before  run ")
        locator=base.__getitem__("进入登陆页面")
        self.basePage.click(locator)


    def teardown_method(self):

        print("every case after  run ")


    def test_001(self,selenium:SeleniumAdapter):
        print('Test_01下的用例001登陆')
        self.seleniumAdapter.assert_true(False,"ERROR********")

    #用于执行不会报错
    @pytest.mark.xfail(reason="Xfail用于预期用例失败，但是不会跳过，结果不会报错")
    def test_002(self):
        print('Test_01下的用例002')
        assert 2 == 3

    #skipif带判断条件的跳过
    @pytest.mark.skipif(sys.platform=='win32', reason='在linux上运行，跳过Windows')
    def test_003(self):
        print('Test_01下的用例003不需要登陆就可执行')
        assert 3 == 3

    #skip直接跳过
    @pytest.mark.skip(reason="用例跳过原因****")
    def test_004(self):
        print('Test_01下的用例004不需要登陆就可执行')
        assert 4 == 3

    @pytest.mark.xfail()
    def test_005(self):
        print('Test_01下的用例005不需要登陆就可执行')
        assert 5 == 5

    #mark用于标记用例，使用命令行可以指定单独用例执行
    def test_006(self):
        print('Test_01下的用例006不需要登陆就可执行')
        assert 5 == 5

    #pytest按照从上到下的顺序执行，使用插件pytest-ordering可以指定用例执行顺序
    @pytest.mark.run(order=2)
    def test_007(self):
        print('Test_01下的用例007不需要登陆就可执行')
        assert 5 == 5


    @pytest.mark.run(order=3)
    def test_008(self,browser):
        print('Test_01下的用例008不需要登陆就可执行')
        time.sleep(2)
        browser.get("https://www.gushiwen.cn/")
        assert browser.title == "古诗文网-古诗文经典"

    a=1
    # 用例失败重跑,使用pytest-rerunfailures插件,可以通过装饰器加到类或方法上
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_009(self):
        print('Test_01下的用例008不需要登陆就可执行')
        self.a = self.a + 1
        assert 3 == self.a

    #使用pytest-repeat插件可以重复执行用例
    @pytest.mark.repeat(2)
    def test_010(self):
        print('Test_01下的用例010不需要登陆就可执行')


if __name__ == '__main__':
    #使用分布式插件执行pytest-xdist
    pytest.main(['-vsm'])