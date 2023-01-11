# -- coding: utf-8 --
import pytest
import allure_pytest

if __name__ == '__main__':
    pytest.main(['-v','-s','./TestSuites/test_demo.py::TestClass::test_001',
                '-capture=sys',
                 '--driver=CHROME',
                 '--driver-path=F:\\pythonLearn\\com\\yang\\practice100\\POM\\Utils\\driver\\chromedriver.exe',
                 '--capability','browserName','chrome',
                 '--alluredir=./results/reports'])