#__author__ = "kirry"

from flask import Flask

app = Flask(__name__)


class Base(object):

    BROWERS = "chrome"
    HTTP = "http"
    HOST = "192.168.1.12"
    PATH = "fone/UserLogin.html"
    SERVER_URL = HTTP+"://"+HOST+"/"+PATH
    USER_NAME = "296795065@qq.com"
    PASSWD = "123456"



    #清理后台应用exe，为空则不清理
    CLEAR_EXE = False and [
        "chromedriver.exe","chrome.exe","geckodriver.exe","firefox.exe",
        "IEDriverServer.exe","iexplore.exe"
    ]





class user001(Base):
    USER_NAME = ""
    PASSWD = ""






config_data = {
    "default":Base(),
    "user001":user001()
}