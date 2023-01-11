# -- coding: utf-8 --
import pytest

if __name__ == '__main__':
    pytest.main(["-s","-v","--capture=sys","--driver==Chrome"
                 ,"--driver-path=F:\\pythonLearn\\com\\yang\\practice100\\POM\\Utils\\driver\\chromedriver.exe"
                 ,"--capability","browserName","chrome"
                 ,"--html=./report/report.html","--self-contained-html"
                 ,"."])