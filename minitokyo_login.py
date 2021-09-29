from selenium import webdriver


url = 'http://my.minitokyo.net/login'
driver = webdriver.Chrome()  #chrome_options=chrome_options)
driver.get(url)
password = driver.find_element_by_xpath('//*[@id="content"]/form/li[2]/input')
password.send_keys('aaaaaaaaa')
log_in = driver.find_element_by_xpath('//*[@id="content"]/form/li[3]/input')
log_in.click()

