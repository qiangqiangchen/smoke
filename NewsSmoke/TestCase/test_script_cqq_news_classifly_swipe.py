# -*- coding:utf-8 -*-
# Author : 陈强强
#TestCase: 新闻-新闻分类-查看未显示的新闻分类
#TestResult:1.可以看到未显示的新闻分类
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
    
    def test_script(self):
        #操作步骤
        classiflylist=[]
        #点击发现  tab
        me_btn=self.driver.find_element_by_name("发现")
        if me_btn.is_displayed():
            me_btn.click()
            sleep(T*1)
            
        #点击新闻
        self.driver.find_element_by_id("tech.yunjing.biconlife.app.find:id/rl_found_news").click()
        sleep(T)
        
        #断言是否进入新闻页面
        assert u"首页"==self.driver.find_element_by_id('tech.yunjing.biconlife:id/tv_ljtb_title').text
        
        
        #点击添加按钮
        self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/iv_nha_channelAdd').click()
        sleep(T)
        
        #断言是否进入栏目页面
        assert u"栏目"==self.driver.find_element_by_id('tech.yunjing.biconlife:id/tv_ljtb_title').text
        
        #点击编辑按钮
        self.driver.find_element_by_name(u'编辑').click()
        sleep(T)
        
        #判断是否存在栏目
        remove_news_count=len(self.driver.find_elements_by_id('tech.yunjing.biconlife.app.news:id/iv_remove_news'))
        if remove_news_count>1:
            #删除之前添加的分类
            for i in range(remove_news_count):
                self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/iv_remove_news').click()
                sleep(1)
                
            #添加10个分类
            for i in range(10):
                self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/tv_name_un').click()
                sleep(1)
        else:
            #添加10个分类
            for i in range(10):
                self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/tv_name_un').click()
                sleep(1)
        #点击完成按钮
        self.driver.find_element_by_name('完成').click()  
        
        sleep(T)
        
        #将添加的栏目加入classiflylist
        content=self.driver.find_elements_by_id('tech.yunjing.biconlife.app.news:id/tv_name_selected_news')
        for i in content:
            classiflylist.append(i.text)
        
        #点击完成按钮
        self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/tv_action').click()  
        sleep(T)
        

        #返回到首页
        self.driver.find_element_by_id('tech.yunjing.biconlife:id/iv_ljtb_left_back').click()
        sleep(T)
        
        
        #获取滑动控件，计算滑动范围
        viewTab=self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/hs_nha_viewTabs')
        viewTab_location=viewTab.location
        viewTab_size=viewTab.size
        
        x1=viewTab_location['x']+viewTab_size['width']*0.8
        x2=viewTab_location['x']+viewTab_size['width']*0.2
        y=viewTab_location['y']+viewTab_size['height']*0.5
        
        #滑动操作
        
        
        #设置标志位，当滑动分类可以找到添加的最后一个元素时就判断成功
        Flag=False
        
        #循环滑动，页面的分类列表，判断最后一条分类是否和添加的最后一个相同，相同则退出循环
        index=0
        while index<10:
            
            classiflys=self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/hs_nha_viewTabs').find_elements_by_class_name('android.widget.TextView')
            if classiflys[-1].text == classiflylist[-1]:
                #print 'The match is successful'
                Flag=True
                break
            else:
                self.driver.swipe(x1, y, x2, y, 2000)  
                index+=1
                    
        if not Flag:
            print 'not found'  
            
        assert Flag==True
         
        #==============================================
        #清空添加的分类
           
        #点击添加按钮
        sleep(T)
        self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/iv_nha_channelAdd').click()
        sleep(T)
        
        #点击编辑按钮
        self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/tv_action').click()
        sleep(T)
        #逐个删除添加的分类
        remove_news_count=len(self.driver.find_elements_by_id('tech.yunjing.biconlife.app.news:id/iv_remove_news'))
        for i in range(remove_news_count):
            self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/iv_remove_news').click()
            sleep(1)
        #点击完成按钮
        self.driver.find_element_by_id('tech.yunjing.biconlife.app.news:id/tv_action').click()  
        sleep(1)
             
     
        
              
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_script)
    unittest.TextTestRunner(verbosity=2).run(suite)