#__author__ = "kirry"


from HTMLTESTRunner.Method.common import webdriver,Chrome,Firefox,Ie,phantomjs,Chrome_headless
import time
import os
import datetime
from HTMLTESTRunner.config import app,config_data
import threading
filepath = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]



class F_OneMethod(object):

    def __init__(self,user="default"):
        app.config.from_object(config_data[user])
        self._lock = threading.Lock




    def F_One_driver(self,browser="chrome",timeout=15):
        '''
        :param browser: 浏览器名字分别为chrome，firefox，Ie
        :return: driver
        '''
        print("开始运行时间为 %s"%time.ctime())
        print("当前浏览器为%s"%browser)
        url = app.config["SERVER_URL"]
        if browser == "chrome":
            driver = Chrome(service_log_path=os.path.join(filepath,"log","chromedriver.log"))
        elif browser == "firefox":
            driver = Firefox(log_path=os.path.join(filepath,"log","firefoxdriver.log"))
        elif browser == "Ie":
            driver = Ie(log_file=os.path.join(filepath,"log","Iedriver.log"))
        elif browser == "phantomjs":
            driver = phantomjs(service_log_path=os.path.join(filepath,"log","phantomjsdriver.log"))
        elif browser == "chrome_headless":
            driver = Chrome_headless(service_log_path=os.path.join(filepath,"log","chrome_headless.log"))
        else:
            raise Exception("brower参数不能为空！")
        driver.get(url)
        driver.maximize_window()
        webdriver(driver).wait_driver(timeout)
        return driver




    def Login(self,driver,companyName="上海绎维软件系统有限公司",timeout=15):
        '''
        :param driver: 浏览器驱动
        :param companyName: 公司名称
        :param timeout: 登录超时时长
        :return:
        '''
        user = app.config["USER_NAME"]
        passwd = app.config["PASSWD"]
        try:
            self.wb = webdriver(driver)
            self.wb.find_element("#txtAccount").clear()
            self.wb.find_element("#txtAccount").send_keys(user)
            self.wb.find_element("#passwordInput").clear()
            self.wb.find_element("#passwordInput").send_keys(passwd)
            self.wb.find_element("#loginButton>lan").click()
            self.wb.wait_notEle_time(".pleaseWait",timeout)
            companyEle = self.wb.find_element("#login_selectCompany")
            if not companyEle.is_displayed():
                raise Exception("用户%s登录密码%s后未显示公司选项！"%(user,passwd))
            companyEle.click()
            companyEles = self.wb.find_elements("#login_selectCompany>ul>li")
            for i in companyEles:
                if i.text == companyName:
                    i.click()
                    break
                else:
                    raise Exception("用户%s登录密码%s后未显示%s公司选项！"%(user,passwd,companyName))
            self.wb.find_element("#loginButton>lan").click()
            self.wb.wait_notEle_time(".pleaseWaitStyle",timeout)
        except:
            raise Exception("用户%s登录密码%s失败！请检查元素或者账号是否正确！"%(user,passwd))
        return driver




    def enter_platform_application(self,platform_name,serach = None,timeout = 15):
        '''
        :param platform_name: 平台应用名称
        :param serach: 查询的平台应用名称
        :return: driver
        '''
        self.wb.find_element(".customLink.sapUiLnk").click()
        if serach:
            serach_input = self.wb.find_element(".sapUiTf.sapUiTfInner")
            serach_input.clear()
            serach_input.send_keys(serach)
            platform_eles = self.wb.find_elements(".sapUiVltCell.sapuiVltCell>.SelectableList>div")
            for platform_ele in platform_eles:
                if serach not in platform_ele.text:
                    raise Exception("通过查询条件查询应用名称%s失败！"%platform_name)
        platform_eles = self.wb.find_elements(".sapUiVltCell.sapuiVltCell>.SelectableList>div")
        try:
            for platform_ele in platform_eles:
                if platform_ele.text == platform_name:
                    platform_ele.click()
                    break
        except:
            raise Exception("点击进入%s平台应用失败！"%platform_name)
        driver = self.wb.driver()
        curent_handle = driver.current_window_handle
        handles = driver.window_handles
        for i in handles:
            if curent_handle != i:
                driver.close()
                driver.switch_to.window(i)
                self.wati_for_package(timeout)
        else:
            return driver



    def enter_right_application(self,right_name,timeout = 15):
        '''
        :eg:进入右侧导航页面
        :param right_name:导航页面名称
        :param timeout: 页面加载时间
        :return:
        '''
        rightELes = self.wb.find_elements(".sapUiUx3ShellHeaderTitleRight>button>img")
        for index,i in enumerate(rightELes):
            text = i.get_attribute("alt")
            if text == right_name:
                i.click()
                if index ==4:
                    driver = self.wb.driver()
                    curent_handle = driver.current_window_handle
                    handles = driver.window_handles
                    for i in handles:
                        if curent_handle != i:
                            driver.switch_to.window(i)
                self.wati_for_package(timeout)
                break
        else:
            raise Exception("F_one首页页面右边没有导航按钮")
        return True




    def chreate_new_work(self,wrokName,chreateName,url=None,filepath=None,timeout=5):
        '''
        :param wrokName: 新建文件名称
        :param url:新建链接地址
        :param chreateName:创建文件件输入的名称
        :param filepath:新建文本上传文件路径
        :return:
        '''
        serachbutton = self.wb.find_element(".customLabelRightIcon>img")
        serachbutton.click()
        serachlist = self.wb.find_elements(".sapUiLbxITxt")
        self.wb.wait_ele_time(".sapUiLbxITxt",1)
        for i in serachlist:
            if i.text==wrokName:
                i.click()
                break
        else:
            raise Exception("通过文件类型查询文件列表失败，未找到%s选项！"%wrokName)
        searchinput = self.wb.find_elements(".sapUiTf.sapUiTfInner")[-1]
        searchinput.send_keys(chreateName)
        self.wati_for_package(timeout)
        elelist = self.wb.find_elements(".sapUiUx3DSItems>div>div")[:-1]
        for i in elelist:
            '''
            -----
            昨日停止位置
            -----
            '''
            texts = i.find_element_by_css_selector("div>.TileItemHeader>span")
            if chreateName == texts.text:
                raise Exception("当前创建文件名称已经存在！")
        self.wb.driver().refresh()
        self.wati_for_package(timeout)
        self.wb.find_elements(".sapUiTbInnerRight>button")[-1].click()
        self.wati_for_package(timeout)
        elelist = self.wb.find_elements("[role='listbox']>li")
        if elelist:
            for i in elelist:
                if i.text == wrokName:
                    if i.text in ["链接","文件"]:
                        i.click()
                        self.wati_for_package(timeout)
                        if i.text == "链接":
                            inputs = self.wb.find_elements("#sap-ui-static>div>div>div>div>div>div>input")
                            button = self.wb.find_element(".sapUiDlgBtns>button:nth-child(1)")
                            if url:
                                inputs[0].send_keys(chreateName)
                                inputs[1].send_keys(url)
                                button.click()
                                self.wati_for_package(timeout)
                            else:
                                raise Exception("创建新链接参数缺少url！")
                        else:
                            uploadfile = self.wb.find_element("#sap-ui-static>div>div>div>div>div>div>input")
                            button = self.wb.find_element(".sapUiDlgBtns>button:nth-child(1)")
                            if filepath:
                                uploadfile.send_keys(filepath)
                                button.click()
                                self.wati_for_package(timeout)
                            else:
                                raise Exception("创建上传文件参数缺少文件上传路径filepath！")
                    else:
                        i.click()
                        self.wati_for_package(timeout)
                        inputele = self.wb.find_element(".sapUiHLayoutChildWrapper>input")
                        button = self.wb.find_element(".sapUiDlgBtns>button:nth-child(1)")
                        inputele.clear()
                        inputele.send_keys(chreateName)
                        button.click()
                        self.wati_for_package(timeout)
                    break
            searchinput = self.wb.find_element("#__jsview0searchInput-tf-input")
            searchinput.send_keys(chreateName)
            elelist = self.wb.find_elements("#__jsview0_fView>div")
            for i in elelist:
                texts = i.find_element_by_css_selector(".TileItemHeader>span")
                if chreateName == texts.text:
                    break
            else:
                raise Exception("在目录页面创建文件失败，创建后的文件未生成！")
        else:
            raise Exception("目录页面中点击新建按钮后，未弹出列表框！")




    def del_work(self,stypeName,workname):
        '''
        :param workname: 需要删除文件
        :return:
        '''
        serachbutton = self.wb.find_element(".customLabelRightIcon>img")
        serachbutton.click()
        serachlist = self.wb.find_elements("#__box39-list>div>ul>li")
        self.wb.wait_ele_time("#__box39-list",1)
        for i in serachlist:
            if i.get_attribute("title")==stypeName:
                i.click()
                break
        else:
            raise Exception("通过文件类型查询文件列表失败，未找到%s选项！"%stypeName)
        searchinput = self.wb.find_element("#__jsview0searchInput-tf-input")
        searchinput.send_keys(workname)
        elelist = self.wb.find_elements("#__jsview0_fView>div")
        for i in elelist:
            texts = i.find_element_by_css_selector(".TileItemHeader>span")
            if workname == texts.text:
                buttons = i.find_element_by_css_selector(".TileItemfooter>button")
                for i in buttons:
                    if i.get_attribute("title")=="删除":
                        i.click()
                        break
                break
            else:
                raise Exception("文件夹列表页面没有%s该文件，删除失败！"%workname)









    def ClearBrowser(self,names):
        '''
        :param names: exe运行程序名称
        :return:
        '''
        if not isinstance(names,list):
            raise Exception("请求数据格式错误！")
        for i in names:
            try:
                os.system("taskkill /f /im %s"%i)
            except Exception as e:
                raise Exception("当前执行关闭程序命令失败，错误信息为：%s"%e.__str__())
        else:
            print("已关闭"+",".join(names)+"后台程序！")



    def get_pic(self,cls,filename):
        '''
        :return: 截图
        '''
        if isinstance(cls,object):
            filepath = os.path.join(os.path.abspath("ErrorPicture"),cls.__module__.split(".")[-1])
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            filename = filename+datetime.datetime.now().strftime("%Y-%m-%d_%H-%S-%M")+".png"
        else:
            return False
        return self.wb.get_picture(os.path.join(filepath,filename))



    def wati_for_package(self,timeout):
        '''
        :param timeout: 页面隐形等待
        :return: 返回等待
        '''

        return  self.wb.wait_notEle_time(".pleaseWaitStyle",timeout)



    def raise_error(self,errolist):
        '''
        :param errolist: 错误信息列表
        :return:抛出Exception错误
        '''
        if errolist:
            raise Exception("\n".join(errolist))
        else:
            print("测试结束，case正常运行！")


    def assert_error(self,errorlist):
        '''
        :param errorlist: 错误信息列表
        :return: 抛出assertion错误
        '''
        if errorlist:
            assert False,"\n".join(errorlist)
        else:
            print("测试结束，case正常运行！")


