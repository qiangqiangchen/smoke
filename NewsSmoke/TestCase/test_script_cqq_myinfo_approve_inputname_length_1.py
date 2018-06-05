# -*- coding:utf-8 -*-
# Author : 陈强强
#TestCase: 个人资料-实名认证-身份证号码输入正确，姓名输入10个汉字，点击“下一步”
#DateTime: 2018-3-14

import unittest
from appium import webdriver
from time import sleep
import os

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

#延时时间
T = 2

class test_script(unittest.TestCase):
    
    def setUp(self):  
        os.popen("adb uninstall io.appium.android.ime")   
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['deviceName'] = 'MXF0215826004374'
        #desired_caps['app'] = 'C:\\Users\\root\\Downloads\\app-release.apk'
        desired_caps['appPackage'] = 'tech.yunjing.biconlife'
        desired_caps['appActivity'] = 'tech.yunjing.biconlife.LaunchActivity'
        
        #启动appium的输入法
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(10)
        

    def tearDown(self):
        
        self.driver.quit()
        #卸载appium输入法
        os.popen("adb uninstall io.appium.android.ime")
        
    #滑动查找指定元素并点击
    # item_name：元素的name属性  
    def _find_by_scroll(self,item_name):
        item=self.driver.find_element_by_android_uiautomator(
            'new UiScrollable(new UiSelector().scrollable(true).instance(0)).getChildByText(new UiSelector().className("android.widget.TextView"), "'
            + item_name + '")'
            ) 
        item.click() 
            
    """
    The id number is entered correctly, the name is entered in 10 Chinese characters, and click "next".
    """
    def test_script(self):
        #操作步骤
        
        #点击我的  tab
        me_btn=self.driver.find_element_by_name("我的")
        if me_btn.is_displayed():
            me_btn.click()
            sleep(T*1)
            
        #滑动后点击实名认证
        self._find_by_scroll('实名认证')
        sleep(T)
        

        #点击立即认证按钮
        is_not_approve=False
        try:
            now_approve=self.driver.find_element_by_id('tech.yunjing.biconlife.app.mine:id/tv_uaa_right_now_approve')
            is_not_approve=True
            now_approve.click()
            sleep(T)
        except:
            is_not_approve=False
            
        if is_not_approve:
            #姓名输入框输入9个汉字
            
            edt_uia_name=self.driver.find_element_by_id('tech.yunjing.biconlife.app.mine:id/edt_uia_name')
            edt_uia_name.send_keys(u"一二三四五六七八九十")
            sleep(T)
        
            #验证汉字是否为9个汉字
            assert edt_uia_name.text==u'一二三四五六七八九十'
        
            #输入正确的身份证号码
            self.driver.find_element_by_id('tech.yunjing.biconlife.app.mine:id/edt_uia_id_card').send_keys(u'52242619811105565x')
            sleep(T)
        
            #点击下一步按钮
            self.driver.find_element_by_id('tech.yunjing.biconlife.app.mine:id/tv_uia_next_step').click()
        
            #停留3秒后断言请上传身份证资料是否显示
            sleep(T*2)
            page_content=self.driver.find_element_by_name(u"请上传身份证资料")
            assert page_content.is_displayed()==True
        else:
            print "approve pass"
            assert is_not_approve==True
           
        
        
              
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_script)
    unittest.TextTestRunner(verbosity=2).run(suite)