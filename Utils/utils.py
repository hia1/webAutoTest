# -- coding: utf-8 --

import random
import string
import time


def gen_random_string(pre_fix='test_', str_len=10):
    return pre_fix + ''.join(
        random.choice(string.digits + string.ascii_letters) for _ in range(str_len - len(pre_fix)))


def gen_random_num(pre_fix='181', str_len=11):
    return pre_fix + ''.join(random.choice(string.digits) for _ in range(str_len - len(pre_fix)))


def replace_file_content(file, old_content, new_content):
    """
    替换文件内容
    file: 要替换内容的文件路径
    old_content:要替换的内容，可迭代对象，如列表等
    new_content:替换后的内容，可迭代对象，如列表等
    """
    replaces = zip(old_content, new_content)
    with open(file, encoding='utf-8') as fr:
        content = fr.read()
        for old, new in replaces:
            content = content.replace(old, new)
    with open(file, 'w', encoding='utf-8') as fw:
        fw.write(content)


def unicode():
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)


def create_name(n):
    """随机生成n个汉字"""
    name = ''
    for i in range(n):
        s = unicode()
        name = name + s
    return name


def create_digits(n):
    """随机生成n个特殊字符"""
    seed = "!@#$%^&*()+=-"
    sa = []
    for i in range(n):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def create_letters(n):
    """随机生成n个随机生成英文字母"""
    name = ''
    for i in range(n):
        s = random.choice(string.ascii_letters)
        name = name + s
    return name


def wait_util_success(count=10, interval=0.5):
    """装饰器，用作循环等待函数执行成功，若超时则抛异常"""

    def wrapper(func):
        def decorater(*args, **kwargs):
            for i in range(count):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == count - 1:
                        raise Exception(e)
                time.sleep(interval)

        return decorater

    return wrapper
#assert方法增强
class SeleniumAdapter:
    def __init__(self,driver) -> None:
        '''适配器，提供driver、断言、截图功能'''
        self.driver=driver
        self.captures=[]
    def assert_true(self,expr,message):
        try:
            screenshot=self.driver.get_screenshot_as_base64()
            self.captures.append({"type":"screenshot",
                                  "data":screenshot,
                                  "desc":message})
        except Exception as e:
            self.captures.append({"type":"logs",
                                  "data":"WARNING:Failed to gather screenshot"})
        finally:
            assert expr,message

if __name__ == '__main__':
    replace_file_content(
        'results/reports/allure_json/207b0bb4-9969-4e95-bbfa-90b2210a429d-attachment.txt',
        ['[32m', '[0m', '[1m', '[31m', '[33m'], ['' for _ in range(5)])