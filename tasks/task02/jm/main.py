from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('C:\\Users\\choja\\chromedriver\\chromedriver.exe')
driver.get('https://leetcode.com/accounts/login/')

def login(user_id, user_pw):
    driver.find_element_by_name('login').send_keys(user_id)
    driver.find_element_by_name('password').send_keys(user_pw)
    sleep(2)
    driver.find_element_by_xpath('//*[@id="signin_btn"]/div').click()

login('id', 'password')
