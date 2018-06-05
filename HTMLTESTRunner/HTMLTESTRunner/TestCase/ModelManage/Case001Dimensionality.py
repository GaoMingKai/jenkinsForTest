from HTMLTESTRunner.Method.F_OneMethod import F_OneMethod
from HTMLTESTRunner.Method.common import webdriver
import unittest
import time




class Case001(unittest.TestCase):
    '''
    eg:测试项目的
    '''
    buzName = "测试项目的"


    def setUp(self):
        self.error = []
        self.a = F_OneMethod()
        self.driver = self.a.F_One_driver()
        self.driver = self.a.Login(self.driver)

    def tearDown(self):
        self.driver.quit()


    def test_dimensionality(self):
        self.a.enter_platform_application("审批应用0326",timeout=5)
        self.a.enter_right_application("目录")
        self.a.chreate_new_work("多维模型","test",timeout=15)
        self.a.del_work("多维模型","test")









if __name__ == '__main__':
    unittest.main()
