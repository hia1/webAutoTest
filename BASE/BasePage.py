# -- coding: utf-8 --
'''PO层 web UI 自动化基础接口封装'''
import os
from urllib import parse
import time
import base64
import allure
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from POM.Utils.times import dt_strftime
from POM.commom.readConfig import conf
from POM.Utils.logger import log, Log
from POM.commom.readElement import Element
from POM.config.config import cm
from selenium.webdriver.chrome.options import Options as chrome_op
from selenium.webdriver.firefox.options import Options as firefox_op
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


base=Element("base")

class BasePage():
    def __init__(self,driver=None):
        self.log = Log().logger
        self.report=cm.allure_json
        self.broswer=conf.web_broswer or "firefox"
        self.base_url=conf.web_url
        self.timeout = 6
        if driver is None:
            self.set_driver(self.broswer)
        else:
            self.driver=driver
            self.wait = WebDriverWait(self.driver,self.timeout)
            self.action_chain=ActionChains(self.driver)
            self.refresh()


    def set_driver(self,driver):
        '''设置浏览器相关参数'''
        if "chrome" == driver.lower().strip():
            options = chrome_op()
            options.add_argument('--start-maxmized')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-eroors')
            self.driver = webdriver.Chrome(os.path.join(cm.DRIVER_PATH,'chromedriver'),chrome_options=options)
        elif 'firefox' == driver.lower().strip():
            binary_file=conf.firefox_binary or '/usr/bin/firefox-esr'
            excutable_path=os.path.join(cm.DRIVER_PATH,'geckodriver')
            options = firefox_op()
            options.binary=FirefoxBinary(binary_file)
            service=Service(executable_path=excutable_path)
            firefox_profile = webdriver.FirefoxOptions()
            firefox_profile.accept_insecure_certs=True
            self.driver=webdriver.Firefox(firefox_profile=firefox_profile,options=options,service=service)
            self.driver.maximize_window()
        else:
            raise Exception("暂不支持%s浏览器驱动"%self.driver)
        self.wait=WebDriverWait(self.driver,self.timeout)
        #ActionChains模拟鼠标操作
        self.action_chain=ActionChains(self.driver)


    '''检验webdriver时候quit'''
    def check_driver_quit(self):
        if self.driver.service.process is not None:
            return False
        return True


    def get_url(self,url):
        '''打开URL'''
        url = parse.urljoin(self.base_url,url)
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.implicitly_wait(self.timeout)
            self.driver.get(url)
            self.log.info("open page %s" % url)
        except TimeoutException:
            self.driver.quit()
            raise TimeoutException("open page (%s) timeout,please check internet")
    #"关闭浏览器"
    def quit_browser(self):
        self.driver.close()


    # @staticmethod用于修饰类中的方法，使其可以再不创建类实例的情况下调用方法，这样做的好处是执行效率较高，当然也可像一般方法一样用实例调用该方法。该方法一般被成为静态方法。
    @staticmethod
    def element_loactor(func,locator):
        '''元素定位器'''
        name,vlue=locator
        return func(cm.LOCATE_MODE[name],vlue)

    def find_element(self,locator):
        '''获取单个元素'''
        ele=BasePage.element_loactor(lambda *args:self.wait.until(EC.presence_of_element_located(args)),locator)
        return ele

    def find_elements(self,locator):
        '''获取多个相同元素'''
        eles=BasePage.element_loactor(lambda *args:self.wait.until(EC.presence_of_all_elements_located(args)),locator)
        return eles

    def elements_num(self,locator):
        '''查找多个相同的元素的个数'''
        num=len(self.find_elements(locator))
        self.log.info("same element:{}".format(locator,num))
        return num

    def find_element_clickable(self,locator):
        '''返回可点击的元素'''
        onclick=BasePage.element_loactor(lambda *args:self.wait.until(EC.element_to_be_clickable(args)),locator)
        return onclick

    def find_element_by_element(self,element,locator):
        """通过已知元素查找相关元素,locator"""
        name,value =locator
        if name != By.XPATH:
            raise Exception("this func support By.XPATH only")
        if value.startwith('/'):
            value='.'+value
        ele=WebDriverWait(element,self.timeout).until(EC.presence_of_element_located((name,value)))
        return ele


    def alert_is_present(self):
        """告警窗口出现"""
        return EC.alert_is_present()(self.driver)


    def input_text(self,locator,txt):
        '''输入事件'''
        if isinstance(locator,WebElement):
            ele = locator
        else:
            ele=self.find_element(locator)
        time.sleep(0.5)
        ele.clear()
        time.sleep(0.5)
        if txt=="":
            ele.send_keys('a')
            time.sleep(0.5)
            ele.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
        ele.send_keys(txt)
        self.log.info("input text:{}".format_map(txt))
        return ele

    def reset_actions(self):
        """清除存储在action_chain的动作"""
        self.action_chain.reset_actions()
        time.sleep(1)

    def click(self,locator):
        """点击"""
        if isinstance(locator,WebElement):
            ele=locator
        else:
            ele=self.find_element_clickable(locator)
        ele.click()
        time.sleep(0.5)
        self.log.info("click element:{}".format(locator))
        return ele

    def wait_alert(self,interval=0.5,wait_couunt=10):
        '''等待alert弹窗出现'''
        while wait_couunt>0:
            result=self.alert_is_present()
            if result is not False:
                return result
            time.sleep(interval)
            wait_couunt-=1
        raise Exception("wait alert time out!")

    def get_alert_text(self,interval=0.5,wait_couunt=10):
        '''获取alert告警内容'''
        alert=self.wait_alert(interval=interval,wait_couunt=wait_couunt)
        self.log.info("get alert content")
        return alert.text

    def accept_alert(self,interval=0.5,wait_couunt=10):
        """告警确定"""
        alert=self.wait_alert(interval=interval,wait_couunt=wait_couunt)
        content = alert.text
        alert.accept()
        self.log.info("accept alerrt: {}".format(alert))
        return content

    def dismis_alert(self,interval=0.5,wait_couunt=10):
        "告警取消"
        alert = self.wait_alert(interval=interval, wait_couunt=wait_couunt)
        content=alert.text
        alert.dismiss()
        self.log.info("alert dismiss: {}".format(alert))
        return content

    def hover(self,locator):
        '''鼠标悬停'''
        if isinstance(locator,WebElement):
             ele=locator
        else:
            ele=self.find_element(locator)
        self.action_chain.move_to_element(ele)
        self.action_chain.perform()
        time.sleep(0.5)
        self.log.info("hover element :{}".format(locator))
        return ele

    def move_mouse(self,xoffset,yoffset):
        """鼠标移动到距离当前位置（x,y）"""
        self.action_chain.move_by_offset(xoffset,yoffset).perform()
        time.sleep(0.5)
        self.log.info("mouse move ({},{}) ".format(xoffset,yoffset))

    def enter(self,locator):
        '''回车元素 '''
        if isinstance(locator,WebElement):
            ele=locator
        else:
            ele=self.find_element(locator)
        ele.send_keys(Keys.ENTER)
        time.sleep(0.5)
        self.log.info('enter ele :{}'.format(locator))
        return ele

    def element_text(self,locator):
        """获取当前的text"""
        if isinstance(locator,WebElement):
            ele=locator
        else:
            ele=self.find_element(locator)
        text=ele.text
        self.log.info("get text:{}".format(text))
        return text.strip()

    def assert_result(self,result,expect=True,not_negative=True,msg=''):
        """断言,not_negative=True表示正向逻辑
        result =True or result =False 也可以一个元组或列表"""
        if isinstance(expect,bool):
            if not_negative and (result==expect):
                assert True
            elif (not not_negative) and (result!=expect):
                assert True
            else:
                self.save_screenshot(msg)
                self.log.error(msg,exc_info=True)
                assert False
        else:
            if not_negative and (expect in result):
                assert True
            elif (not not_negative) and (expect not in result):
                assert True
            else:
                self.save_screenshot(msg)
                self.log.error(msg,exc_info=True)
                assert False

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        time.sleep(0.5)

    def save_screenshot(self,msg):
        """截图并保存"""
        if '/' in msg:
            msg=msg.replace('/','-')
        file_name=dt_strftime(fmt='%Y%m%d%H%M%S')+ '-' + str(msg) + '.png'
        file = os.path.join(self.report, file_name)
        self.driver.save_screenshot(file)
        allure.attach.file(file,file_name,attachment_type=allure.attachment_type.PNG)

    @property
    def success(self):
        return True

    @property
    def fail(self):
        return False

    def select(self,locator,by_type,type_val):
        '''下拉菜单选择by_type:
        value --> select_by_value
        index --> select_by_index
        type_val: 对应于by_type的对象值'''
        if isinstance(locator,WebElement):
            ele=locator
        else:
            ele=self.find_element(locator)
        s=Select(ele)
        if by_type=='value':
            s.select_by_value(type_val)
        elif by_type=='index':
            s.select_by_index(type_val)
        elif by_type=="text":
            s.select_by_visible_text(type_val)
        else:
            raise Exception('by_type is enum:value/index/text')
        self.log.info("select: {}".format(type_val))
        return s.all_selected_options

    def deselect(self,locator,by_type,type_val):
        '''下拉菜单取消选择by_type:
        value --> deselect_by_value
        index --> deselect_by_index
        type_val: 对应于by_type的对象值'''
        if isinstance(locator,WebElement):
            ele=locator
        else:
            ele=self.find_element(locator)
        s=Select(ele)
        if by_type=='value':
            s.deselect_by_value(type_val)
        elif by_type=='index':
            s.deselect_by_index(type_val)
        elif by_type=="text":
            s.deselect_by_visible_text(type_val)
        else:
            raise Exception('by_type is enum:value/index/text')
        self.log.info("deselect: {}".format(type_val))
        return s.all_selected_options

    def table(self,locator):
        """table表格"""
        if isinstance(locator, WebElement):
            ele = locator
        else:
            ele = self.find_element(locator)
        tr_list=ele.find_elements(By.TAG_NAME,'tr')
        table_info=[]
        table_info.append(tr_list[0].find_elements(By.TAG_NAME,'th'))
        for tr in tr_list[1:]:
            table_info.append(tr.find_element(By.TAG_NAME,'td'))
        return table_info

    def element_li(self,locator,li_text) ->WebElement:
        """判断ul/ol 中的li列表元素"""
        if isinstance(locator, WebElement):
            ele = locator
        else:
            ele = self.find_element(locator)
        self.log.info('get list ele:{}'.format(locator))
        lis=ele.find_elements(By.TAG_NAME,'li')
        for li in lis:
            if li.text.strip() == li_text.strip():
                return li
        raise Exception("can't find ele %s in list" % li_text)

    def select_radio_or_checkbox(self,locator):
        """勾选单选框或复选框"""
        if isinstance(locator, WebElement):
            ele = locator
        else:
            ele = self.find_element(locator)
        if ele.is_selected():
            self.log.info('check :{}'.format(locator))
            return
        self.click(ele)
        if not ele.is_selected():
            self.log.info('check :{} fail'.format(locator))
            raise Exception('check :{} fail'.format(locator))
        self.log.info('check:{}'.format(locator))

    def deselect_checkbox(self,locator):
        """去勾选复选框"""
        if isinstance(locator, WebElement):
            ele = locator
        else:
            ele = self.find_element(locator)
        if ele.is_selected():
            self.click(ele)
        if  ele.is_selected():
            self.log.info(' check back :{} fail'.format(locator))
            raise Exception('check back :{} fail'.format(locator))
        self.log.info('check back:{}'.format(locator))

    def select_by_noselector(self,locator,tag_name,attr_name,*attr_value):
        '''无select标签的下拉菜单选项
         可以通过标签的属性值或者text来定位，也可以通过index来定位
        '''
        if isinstance(locator, WebElement):
            ele = locator
        else:
            ele = self.find_element(locator)
        sels=ele.find_elements(By.TAG_NAME,tag_name)
        selected=[]
        for val in attr_value:
            #通过index定位
            if isinstance(val,int):
                self.click(sels[val])
                selected.append(val)
                self.log.info('select num {}'.format(val))
            else:
                for sel in sels:
                    #获取元素text
                    sel_v=sel.get_attribute(attr_name)
                    if sel_v is None:
                        sel_v=sel.text
                    if sel_v.strip() == str(val).strip():
                        self.click(sel)
                        selected.append(sel_v)
                        self.log.info("select {}".format(val))
                        break
        if len(selected) !=len(attr_value):
            #如下菜单选项未被点击选中
            raise Exception("{} of menu not be selected".format([i for i in attr_value if i not  in selected]))

    def check_confirm_window(self,confirm_content):
        """判断是否弹出确认窗口，如删除XX确认窗口"""
        confirm_window = self.find_element(base['确认弹窗'])
        if confirm_content.strip() not in confirm_window.text:
            raise Exception("alert error,expect content:{},actual content{}".format(confirm_content,confirm_window.text.strip()))
        return confirm_window

    @allure.step('点击确定')
    def accept_confirm(self):
        try:
            self.click(base['确认'])
            self.log.info('点击确认')
            time.sleep(2)
        except:
            self.assert_result(False,msg='点击确认失败')

    @allure.step('点击取消')
    def dismiss_confirm(self):
        try:
            self.click(base['取消'])
            self.log.info('点击取消')
            time.sleep(2)
        except:
            self.assert_result(False,msg='点击取消失败')

    #？
    def get_dd_by_dt(self,locator,*dt):
        _,val =locator
        if not val.endswith('dl'):
            raise Exception("locator must located 'dl'")
        dts={}
        _els=self.find_element(locator)
        for i in dt:
            for ele in _els:
                ele_text=ele.text
                ele_dt=ele_text.split(':')[0].strip()
                if ele_dt == i.strip():
                    ele_dd = ele_text.split(':')[1].strip()
                    self.log.info('{}：{}'.format(ele_dt, ele_dd))
                    dts.update({ele_dt: ele_dd})
                    break
        if len(dts)==len(dt):
            return dts
        not_in=[]
        for i in dt:
            if i.strip() not in dts:
                not_in.append(i)
        raise Exception('dt{} not  exists,please check'.format(not_in))

    def match_by_name(self,table_info,match_word,primary_td=2):
        """默认返回名称为match_word或第match_word行"""
        if isinstance(match_word,int):
            return table_info[match_word]
        for tr in table_info:
            if tr[primary_td].text == match_word:
                self.log.info("find %s "%match_word)
                return tr
        raise Exception('not find %s' %match_word)


    def natch_by_name(self,table_info,match_word,primary_td=2):
        """默认返回名称为match_word或第match_word行"""
        if isinstance(match_word,int):
            return table_info[match_word]
        for tr in table_info:
            if tr[primary_td].text==match_word:
                self.log.info("find ele %s position" %match_word)
                return tr
        raise Exception('can not find name= %s ele of row' %match_word)

    @allure.step('选择搜索类型')
    def select_search_type(self,search_type='名称'):
        '''"""选择搜索类型"""'''
        try:
            self.hover(base['检索类型'])
            search_type_list=self.element_text(base['检索类型列表'])
            if search_type in search_type_list:
                ele_loc=self.element_li(base['检索类型列表'],search_type)
                self.click(ele_loc)
                self.move_mouse(0,-50)
            else:
                raise Exception('检索类型异常')
        except:
            self.assert_result(False,msg='[ERROR]选择搜索类型失败')


    @allure.step('输入查询关键字')
    def input_search_word(self,input_word):
        '''输入查询关键字'''
        try:
            ele=self.input_text(base['输入查询关键字'],input_word)
            self.enter(ele)
            time.sleep(0.5)
        except:
            self.assert_result(False,msg='[ERROR]输入查询关键字失败')

    @allure.step('清空检索项')
    def clear_search(self):
        try:
            self.click(base['清空检索项'])
            time.sleep(0.5)
        except:
            self.assert_result(False,msg='[ERROR]清空检索项失败')


    @allure.step('获取当前界面非法输入提示信息')
    def get_validation_message(self):
        """获取当前界面非法输入提示信息"""
        try:
            messages=self.find_elements(base['验证消息'])
            meg_list=[]
            for meg in messages:
                meg_list.append(self.element_text(meg).strip())
            return ''.join(meg_list)
        except:
            self.assert_result(False,msg="[ERROR]当前界面无验证消息")

    @allure.step('查找当前界面中置灰的按钮')
    def find_disable_eles(self):
        """查找当前界面中置灰的按钮"""
        try:
            ele_list=self.find_elements(base['置灰按钮'])
            ele_texts=[]
            for ele in ele_list:
                ele_texts.append(self.element_text(ele).strip())
            self.log.info('置灰按钮:{}'.format(ele_texts))
            return ''.join(ele_texts)
        except:
            self.assert_result(False,msg="[ERROR]查找当前界面中置灰的按钮失败")



    def excepted_alert(self):
        '''判断弹窗是否存在'''
        login_alert = EC.alert_is_present()(self.driver)
        if (login_alert):
            print("弹窗内容：", login_alert.text)
            return login_alert
        else:
            print("无弹窗")
            return False

    def switch_alert(self):
        '''切换至alert弹窗'''
        alert=self.driver.swich_to.alert()
        return alert


    # iframe切换
    def switch_iframe(self,selector):
        #判断是否存在，存在就跳转
        ifarme=WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it(selector))
        if (ifarme):
            return  ifarme
        else:
            #不存在返回原页面并返回False
            self.driver.swich_to.default_content()
            return False


    #滚动条
    def scrollMove(self,locator,*fun):
        #By.CSS_SELECTOR,定位当前页面顶部位置元素
        element=self.find_element(locator)
        #将页面滚动至底部
        if 'bottom'==fun:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        elif 'top' == fun:
            ##将页面滚动至顶部
            self.driver.execute_script("arguments[0].scrollIntoView(false)", element)
            # 将滚动条滚动到指定位置
        elif type(fun)==tuple:
            self.driver.execute_script("window.scrollTo(%d)"%fun)
        else:
            print('滚动条方法不支持')
            return False
