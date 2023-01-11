# -- coding: utf-8 --
'''用于读取testdata目录下数据驱动配置的Excel数据'''

import os
import pandas as pd
from POM.config.config import cm


class TestData():
    """
    功能:获取excel文件数据
    参数:name:excel文件名称，不包括后缀
        caseid:与Excel文件sheet页名称相同，建议以用例ID命名
    返回:以列表形式返回对应sheet页所有数据
    """

    def __init__(self, name):
        self.file_name =  name
        self.testdata_path = os.path.join(cm.TESTDATA_PATH, self.file_name)
        if not os.path.exists(self.testdata_path):
            raise FileNotFoundError("%s 文件不存在！" % self.testdata_path)
        # ExcelFile同时读取一个文件的多个sheet，仅需读取一次内存，性能更好
        self.testdata = pd.ExcelFile(self.testdata_path, engine='xlrd')


    def __call__(self, caseid):
        return self.testdata.parse(str(caseid), keep_default_na=False).values.tolist()

    #新增方法 yang
    def get_value(self,sheetName):
        self.data=pd.read_excel(self.testdata_path,sheet_name=sheetName)
        return self.data




if __name__ == '__main__':
    td=TestData("casedemo.xls")
    rating=pd.read_excel(td.testdata_path,header=None,index_col=None)
    print(rating.head())
    print(td.__call__("module01"))
    print(td.get_value("module01").iloc[:,:1])


