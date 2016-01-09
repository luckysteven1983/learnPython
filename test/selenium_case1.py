#-*- conding=utf-8 -*-
from selenium import webdriver
if __name__ == "__main__":
    driver = webdriver.Firefox()
    #driver.implicitly_wait(30)
    driver.get("http://www.baidu.com")
    driver.find_element_by_name("wd").send_keys("hello Selenium!")
    driver.find_element_by_name("wd").submit()
    print 'Page title is:',driver.title
    driver.quit()
