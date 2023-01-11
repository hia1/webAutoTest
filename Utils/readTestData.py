# -- coding: utf-8 --
import os

#读取测试数据
def readTestData():
    data_list=[]
    file=open(("testdata.txt"),'r',encoding="utf-8")
    for line in file.readlines():
        data_list.append(line.strip("\n").split(","))
    # print(data_list)
    return data_list
if __name__ == '__main__':
    readTestData()