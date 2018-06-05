#__author__ = "kirry"



from selenium.webdriver.chrome.webdriver import WebDriver as chrome
from selenium.webdriver.firefox.webdriver import WebDriver as firefox
from selenium.webdriver.ie.webdriver import WebDriver as ie
from selenium.webdriver.phantomjs.webdriver import WebDriver as phantomjs
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.common.action_chains import ActionChains as action
from selenium.webdriver.chrome.options import Options as op




def Chrome_headless(service_log_path):
    '''
    :eg: 只适合浏览器版本高于60的chrome
    :param service_log_path: driver日志路径
    :return: 返回去头浏览器
    '''
    chrome_options = op()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    return chrome(chrome_options=chrome_options,service_log_path=service_log_path)





class Chrome(chrome):
    '''
    eg:打开chrome浏览器
    '''



class Firefox(firefox):
    '''
    eg:打开firfox浏览器
    '''



class Ie(ie):
    '''
    eg:打开ie浏览器
    '''



class Phantomjs(phantomjs):
    '''
    eg:打开浏览器去头
    '''



class webdriver(object):


    def __init__(self,driver):
        self.__driver = driver


    def driver(self):
        '''
        :return: 返回driver
        '''
        return self.__driver



    def fix_driver(self,driver):
        '''
        :param driver: 新的页面驱动
        :return:
        '''
        if driver:
            self.__driver = driver
        else:
            return False
        return True


    def find_element(self,css):
        if css:
            return self.__driver.find_element_by_css_selector(css)
        else:
            raise Exception("css定位元素不能为空！")


    def find_elements(self,css):
        if css:
            return self.__driver.find_elements_by_css_selector(css)
        else:
            raise Exception("css定位元素不能为空！")



    def wait_ele_time(self,css,timeout):
        try:
            wait(self.__driver,timeout).until(lambda x:x.find_element_by_css_selector(css).is_displayed())
        except:
            raise Exception("%s元素在%ss内未加载出页面，页面加载超时！"%(css,timeout))



    def wait_notEle_time(self,css,timeout):
        try:
            wait(self.__driver,timeout).until_not(lambda x:x.find_element_by_css_selector(css).is_displayed())
        except:
            raise Exception("%s元素在%ss内未隐藏，页面加载超时！"%(css,timeout))



    def wait_driver(self,timeout):
        '''
        :param timeout: time
        :return: 显性等待时间
        '''
        return self.__driver.implicitly_wait(timeout)


    def click_and_hold(self,ele):
        '''
        :param ele: ele
        :return: 操作鼠标按住不动到某个元素
        '''

        return action(self.__driver).click_and_hold(self.find_element(ele)).perform()


    def context_click(self,ele):
        '''
        :param ele:ele
        :return: 在元素上右击
        '''

        return action(self.__driver).context_click(self.find_element(ele)).perform()

    def double_click(self,ele):
        '''
        :param ele: ele
        :return: 在元素上边双击
        '''

        return action(self.__driver).double_click(self.find_element(ele)).perform()



    def drag_and_drop(self,fromEle,toEle):
        '''
        :param fromEle:主元素
        :param toEle: 目标元素
        :return: 从一个元素的位置，拖至另一个元素位置松开
        '''
        return action(self.__driver).drag_and_drop(self.find_element(fromEle),self.find_element(toEle)).perform()


    def drag_and_drop_by_offset(self,fromEle,x,y):
        '''
        :param fromEle: 主元素
        :param x: 横坐标
        :param y: 纵坐标
        :return: 以坐标的形式拖拽，x,y
        '''
        return action(self.__driver).drag_and_drop_by_offset(fromEle,x,y)


    def move_by_offset(self,x,y):
        '''
        :param x: 横坐标
        :param y: 纵坐标
        :return: 鼠标移动到（x,y）坐标位置
        '''
        return action(self.__driver).move_by_offset(x,y)


    def move_to_element(self,ele):
        '''
        :param ele: 目标元素
        :return: 鼠标移动到元素上
        '''
        return action(self.__driver).move_to_element(self.find_element(ele))


    def move_to_element_with_offset(self,ele,x,y):
        '''
        :param ele: 目标元素
        :param x: 横坐标
        :param y: 纵坐标
        :return: 鼠标移动到目标元素，在移动到x，y上
        '''
        return action(self.__driver).move_to_element_with_offset(self.find_element(ele),x,y)


    def execute_script(self,js):
        '''
        :param js: js语法
        :return: 返回执行结果
        '''

        return self.__driver.execute_script(js)


    def get_picture(self,filepath):
        '''
        :param filepath: 保存图片路径
        :return: 返回保存成功或者失败
        '''
        try:
            self.__driver.save_screenshot(filepath)
        except:
            return False
        else:
            return True

