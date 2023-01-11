# -- coding: utf-8 --
'''读取excel操作步骤'''
import xlrd
from POM.commom.readConfig import conf
from Utils.logger import log


class excel_Reader():

    def __init__(self):
        reader = xlrd.open_workbook(conf.test_case)
        self.reader=reader

    def read_excel(self):
        names = self.reader.sheet_names()
        '''读取步骤，以列表形式保存'''
        step_dict={}
        for name in names:
            #data sheet存放数据
            if (name == 'data'):
                continue
            step_dict[name]=[]
            case_xls = self.reader.sheet_by_name(name)
            for i in range(case_xls.nrows):
                if (i==0): #跳过表头
                    continue
                excelParameter_list=[]
                for j in range(case_xls.ncols):
                    excelParameter_list.append(case_xls.cell_value(i,j))
                mode= model()
                mode.sort=excelParameter_list[0]
                mode.desc=excelParameter_list[1]
                mode.action=excelParameter_list[2]
                mode.searchType=excelParameter_list[3]
                mode.searchvalue=excelParameter_list[4]
                mode.searchindex=excelParameter_list[5]
                mode.validateSource=excelParameter_list[6]
                mode.validateAttr=excelParameter_list[7]
                mode.validateType=excelParameter_list[8]
                mode.validateData=excelParameter_list[9]
                step_dict[name].append(mode)
        data_dict={}
        data_xls=self.reader.sheet_by_name('data')
        for i in range(data_xls.nrows):
            name=data_xls.cell(i,0).value
            data_dict[name]=[]
            for j in range(data_xls.ncols):
                value=data_xls.cell(i,j).value.strip()
                if (j==0) or (value==''):
                    continue
                # print(data_xls.cell(i,j).value)
                data_dict[name].append(eval(value))
        #格式转变
        result=[]
        for case_name in list(step_dict.keys()):
            if step_dict[case_name]:
                data_list=step_dict[case_name]
                num=0
                for data in data_list:
                    result.append({"name":case_name,
                                   "steps":step_dict[case_name],
                                   "data":data,
                                   "desc":"{} {}".format(case_name,num)})
                    num+=1
            else:
                result.append({"name":case_name,
                                   "steps":step_dict[case_name],
                                   "data": {},
                                   "desc":"{} 0".format(case_name)})
        return result



    def parseExcel(self,sheetName,dictName,modelVar):
        parseDataList=[]
        for excelResult in result:
                if sheetName == excelResult.get('name'):
                    # print(excelResult)
                    if dictName in excelResult.keys():
                        for excelData in excelResult.get(dictName):
                            parseData =getattr(excelData,modelVar)
                            # print(parseData)
                            parseDataList.append(parseData)
                        return parseDataList
                    else:
                        log.error("{} 不存在".format(dictName))
                        return None
                else:
                    log.error("{} 不存在".format(sheetName))
                    return None
class model():
    def __init__(self) -> None:
        super().__init__()


if __name__ == '__main__':
    ec=excel_Reader()
    result=ec.read_excel()
    a=ec.parseExcel('module01','steps','searchvalue')
    print(a)




