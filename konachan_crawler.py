# Konachan Main
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as te
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
from datetime import date, timedelta
from lxml import html
import urllib
import re
import pyautogui
import os
import shutil
from tqdm import tqdm

year = '2021'


def download(init_url, img):
    download_folder = 'Konachan.' + re.sub('[-]', '.', init_url.split('%3A')[-1])  # 创建下载文件夹
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    print('start downloading...')
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 '
                             'Firefox/67.0'}
    proxy_url = None  # {'http': 'http://127.0.0.1:1081'}
    for i in tqdm(img):
        url = 'https://konachan.com/post/show/{}'.format(i)         # 图片页面的链接通用格式
        page = requests.get(url, headers=headers, proxies=proxy_url)
        tree = html.fromstring(page.content)
        if tree.xpath('//*[@id="png"]/@href'):                  # 从图片页面获得原图片文件地址
            source = tree.xpath('//*[@id="png"]/@href')         # 根据原图片是否为png格式, 原地址不同
        else:
            source = tree.xpath('//*[@id="highres"]/@href')
        file_name = source[0].split('/')[-1]                    # 从原图片地址的最后一段中获得图片描述的部分
        name = urllib.parse.unquote(file_name)                  # 将其中的url转码为对应字符作为下载的文件名
        name_modify = re.sub('[*:?/|<>"]', '_', name)
        data = requests.get(source[0], headers=headers, proxies=proxy_url)
        with open(os.path.join(download_folder, name_modify), "wb") as file:  # 保存文件
            file.write(data.content)
        time.sleep(3)
    print('Download Succeed')
    return


def date_list(start_date, end_date):
    delta = end_date - start_date
    date_lis = []
    for i in range(delta.days + 1):
        date_lis.append(str(start_date + timedelta(days=i)))
    date_lis = [w.replace('{}-'.format(year), '') for w in date_lis]
    return date_lis


def sln_download(idl):
    # download_directory = 'Konachan_download'
    # if not os.path.exists(download_directory):
    #     os.mkdir(download_directory)
    http_proxy = "127.0.0.1:7890"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(http_proxy))
    # pref = {
    #     'download.default_directory': 'D:\\Konachan_download',
    #     'download.prompt_for_download': False,
    #     'download.directory_upgrade': False,
    #     'safebrowsing.enabled': False
    # }
    # chrome_options.add_experimental_option('prefs', pref)
    driver = webdriver.Chrome() #chrome_options=chrome_options)
    print('start downloading...')
    for _ in tqdm(idl):
        url = 'https://konachan.com/post/show/{}'.format(_)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        try:
            img = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="png"]')))
        except te:
            try:
                img = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="highres"]')))
            except:
                continue
        actions = ActionChains(driver)
        actions.click(img)
        actions.perform()
        time.sleep(1)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(0.8)
        pyautogui.typewrite(['enter'])
        time.sleep(1)
    print('download successful')
    time.sleep(5)
    driver.close()


def move(mdate):
    path = 'C:\\Users\\torum\\Downloads'
    list1 = os.listdir(path)
    list2 = []
    for i in list1:
        if i.startswith('Konachan.com'):
            list2.append(i)
    for m in mdate:
        with open('{}-{}'.format(year, m)) as r:
            pairli = r.read().splitlines()
        folder = 'Konachan.{}.{}'.format(m.split('-')[0], m.split('-')[1])
        if not os.path.exists(os.path.join(path, folder)):
            os.makedirs(os.path.join(path, folder))
        for j in list2:
            name_id = j.split(' ')[2]
            if name_id in pairli:
                shutil.move(os.path.join(path, j), os.path.join(path, folder))


def get_id(cdate):
    id_list = []
    if cdate:
        with open('dl_date_list', 'w') as dl:
            for _ in cdate:
                dl.write('{}\n'.format(_))
        with open('{}_{}'.format(cdate[0], cdate[-1])) as f1:
            id_list += f1.read().splitlines()
    else:
        print('No date file!')
        id_list = []
    return id_list


def check(cdate):
    path = 'C:\\Users\\torum\\Downloads'
    list2 = []
    list3 = []
    list1 = os.listdir(path)
    for w in list1:
        if w.startswith('Konachan.com'):
            list2.append(w.split()[2])
    if len(cdate) > 1:
        with open('{}_{}'.format(cdate[0], cdate[-1]), 'r') as r:
            list3 += r.read().splitlines()
    elif len(cdate) == 1:
        with open('{}-{}'.format(year, cdate[0]), 'r') as r:
            list3 += r.read().splitlines()
    diff = list(set(list3) - set(list2))
    with open('undownloaded', 'w') as f:
        for _ in diff:
            f.write('{}\n'.format(_))
    # print(list2, '\n', len(diff))
    return diff


# d = [x for x in input('please input a date range(month, date, date): ').split()]
# bdate = date_list(date(int('{}'.format(year)), int('{:>2}'.format(d[0])), int('{:>2}'.format(d[1]))),
#                       date(int('{}'.format(year)), int('{:>2}'.format(d[0])), int('{:>2}'.format(d[2]))))
# print(bdate)
# move(bdate)
