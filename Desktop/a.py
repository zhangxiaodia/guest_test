import os,time,unittest
from appium import webdriver
desired_caps={}

desired_caps["platformName"]="Android"
desired_caps["platformVersion"]="5.0.0"
desired_caps["deviceName"]="127.0.0.1:62001"
desired_caps["appPackage"]="com.chaping.fansclub"
desired_caps["appActivity"]="com.chaping.fansclub.module.StartActivity"



driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.find_element_by_id('com.android.calculator2:id/digit1').click()
#driver.find_element_by_id('com.android.calculator2:id/plus').click()
#driver.find_element_by_id('com.android.calculator2:id/digit1').click()
#driver.find_element_by_id('com.android.calculator2:id/equal').click()
 
webdriver.quit() 