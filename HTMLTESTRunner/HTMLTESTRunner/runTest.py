#__author__ = "kirry"

import os,sys
sys.path.append(os.path.abspath(".."))
from HTMLTESTRunner.Method.HTMLTestReportCN import HTMLTestRunner
from HTMLTESTRunner.Method.F_OneMethod import F_OneMethod
import unittest
import datetime
from HTMLTESTRunner.config import app
from HTMLTESTRunner.config import config_data

app.config.from_object(config_data["default"])



commond = sys.argv

#开始运行时清理后台占用程序
names = app.config["CLEAR_EXE"]
if isinstance(names,list):
    F_OneMethod().ClearBrowser(names)


filepath = os.path.abspath(".")
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
resultpath = os.path.join(filepath,"results")
filelist = sorted(os.listdir(resultpath))
if len(filelist) > 5:
    delfile = filelist[:-5]
    for i in delfile:
        delfilepath = os.path.join(resultpath,i)
        os.remove(delfilepath)



case = unittest.TestLoader().discover(start_dir=os.path.join(filepath,"TestCase"),pattern="Case*.py")._tests
case = [i for i in case if i._tests]
tester = commond[1] if len(commond)>1 else "admin"
description = commond[2] if len(commond)>2 else "None"
title = commond[3] if len(commond)>3 else "None"
poolrun = commond[4] if len(commond)>4 else 1

with open(os.path.join(filepath,"results","%s.html"%now),mode="wb") as f:
    run = HTMLTestRunner(suitCase= case,stream=f, verbosity=1,title=title,description=description,tester=tester)
    run.poolthread(int(poolrun))

#用例执行结束时清理后台占用程序
if isinstance(names,list):
    F_OneMethod().ClearBrowser(names)
