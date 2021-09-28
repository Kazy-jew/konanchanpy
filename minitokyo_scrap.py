from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
from tqdm import tqdm


def minitokyo_download(idl):
    http_proxy = "127.0.0.1:7890"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(http_proxy))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    print('start downloading...')
    for _ in tqdm(idl):
        url = 'http://gallery.minitokyo.net/download/{}'.format(_)
        driver.get(url)
        location = driver.find_element_by_xpath('//*[@id="image"]/p/a')
        # location.send_keys(Keys.PAGE_DOWN)
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(100, 100, location).perform()
        actions.context_click()
        actions.perform()
        pyautogui.typewrite(['down', 'down', 'enter'])
        time.sleep(1)
        pyautogui.typewrite(['enter'])
    print('download successful')
    time.sleep(5)
    driver.quit()


while True:
    minitokyo = input('please input an id range (748168< id < 757945), q to quit:')
    minitokyo_list = []
    if minitokyo == 'q':
        exit()
    else:
        minitokyo_id = minitokyo.split(' ')
        minitokyo_delta = int(minitokyo_id[1]) - int(minitokyo_id[0])
        for _ in range(minitokyo_delta+1):
            minitokyo_list.append(str(int(minitokyo_id[0])+_))
        minitokyo_download(minitokyo_list)


