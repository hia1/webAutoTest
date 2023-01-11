# -- coding: utf-8 --
'''用于读取page_element目录下元素定位对象yaml文件配置'''
import os
import yaml

from POM.config.config import cm




class Element():
    def __init__(self,name) -> None:
        self.file_name='%s.yaml' %name
        self.element_path=os.path.join(cm.PAGEELEMENT_PATH,self.file_name)
        if not os.path.exists(self.element_path):
            raise FileNotFoundError("%s 文件不存在" % self.element_path)
        #安全的加载yaml源，并将yanl数据反序列化成dict类型
        with open(self.element_path,encoding="utf-8") as fp:
            self.data=yaml.safe_load(fp)

    def __getitem__(self, item):
        '''获取属性 '''
        data = self.data.get(item)
        if  item in self.data:
            name,value = data
            return name,value
        raise ArithmeticError("{}不存在关键字：{}".format(self.file_name,item))

if __name__ == '__main__':
    ele=Element("base")
    print(ele.data)
    print(type(ele["username"]))
    print(ele.__getitem__("username"))
