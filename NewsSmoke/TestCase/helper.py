# -*- coding:utf-8 -*-

# Author : 陈强强
# Description: 用到的常用方法汇总
# DateTime: 2018-1-18


from appium import webdriver
import sys
import time
import threading
reload(sys)
sys.setdefaultencoding('utf-8')



'''
滑动找到相应的item-name，找到后点击
适用于列表类元素
'''
def find_by_scroll(driver,item_name):
    item=driver.find_element_by_android_uiautomator(
        'new UiScrollable(new UiSelector().scrollable(true).instance(0)).getChildByText(new UiSelector().className("android.widget.TextView"), "'
        + item_name + '")'
        )
    item.click() 

def get_screen_size(driver):
    s=driver.get_window_size()
    return s['width'],s['height']

def swipe_left(driver,duration=2000):
    w,h=get_screen_size(driver)
    driver.swipe(w*0.8,h*0.5,w*0.2,h*0.5,duration)
    
def swipe_right(driver,duration=2000):
    w,h=get_screen_size(driver)
    driver.swipe(w*0.2,h*0.5,w*0.8,h*0.5,duration)
    
def swipe_left_fromRim(driver,duration=2000):
    w,h=get_screen_size(driver)
    driver.swipe(w*1,h*0.5,w*0.2,h*0.5,duration)
    
def swipe_right_fromRim(driver,duration=2000):
    w,h=get_screen_size(driver)
    driver.swipe(0,h*0.5,w*0.8,h*0.5,duration)
    
def swipe_up(driver,duration=2000):
    w,h=get_screen_size(driver)
    driver.swipe(w*0.5,h*0.8,w*0.5,h*0.2,duration)
    
def swipe_down(driver,duration=2000):
    w,h=get_screen_size(driver)
    driver.swipe(w*0.5,h*0.2,w*0.5,h*0.8,duration)   
    
def find_element_scroll(driver,id):
    driver=driver
    id=id
    try:
        element=driver.find_element_by_id(id)
        if element.is_displayed():
            element.click()
    except:
        print"not found"
        swipe_up(driver)
        find_element_scroll(driver, id)
        

def find_element_scroll2(driver,id):
    source=None
    while True:
        element=is_exist(driver, 'id', id)
        if element:
            element.click()
            break
        else:
            if source==driver.page_source:
                print'The content of the page has not changed.' 
                break
            else:
                source=driver.page_source
                swipe_up(driver, 1000)
                
         
def wait_element(driver,tag,content):
    index=0
    while index<10:
        if index<10:
            if is_exist(driver, tag, content):
                print 'found tag '
                break
            else:
                print'not found :%s'%(str(index))
                time.sleep(1)
                index+=1
        else:
            print 'timeout'
            break
            
            
    return is_exist(driver, tag, content)
            
        
            


            
def is_exist(driver,tag,content):
    
    try:  
        if tag=='id':
            element=driver.find_element_by_id(content)
            return element
        if tag=='name':
            element=driver.find_element_by_name(content)
            return element
        if tag=='class':
            element=driver.find_element_by_class_name(content)
            return element
    
    except:
        print '%s: %s is not found'%(tag,content)
        return False
        
        
        
    

    
     