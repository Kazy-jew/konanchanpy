# Konachan crawler core
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as te
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
from lxml import html
import urllib
import re
import pyautogui
import os
from tqdm import tqdm
from url import Web_URL
from koyomi import Calendar


class Page_ID:

    def multi_dates(self, dates):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/92.0.4515.131 Safari/537.36'}
        proxy_url = {'http': 'http://127.0.0.1:7890'}
        # id list of date range
        dates_list = []
        year = Calendar().year
        case = Web_URL.konachan
        for n in dates:
            # id list of a date
            date_list = []
            if os.path.exists('{}-{}'.format(year, n)):
                print('list {} already downloaded...'.format(n))
                with open('{}-{}'.format(year, n), 'r') as r:
                    date_list += r.read().splitlines()
            else:
                for i in range(1, 24):
                    url = case.format(i, year, n)
                    page_ = requests.get(url, headers=headers, proxies=proxy_url)
                    tree = html.fromstring(page_.content)
                    mark_tag = tree.xpath('//*[@id="post-list"]/div[3]/div[4]/p/text()')
                    if not mark_tag:
                        date_list += tree.xpath('//*[@id="post-list-posts"]/li/@id')
                    elif mark_tag == ['Nobody here but us chickens!']:
                        date_list = [w.replace('p', '') for w in date_list]
                        with open('{}'.format(url.split('%3A')[-1]), 'w') as f:
                            for item in date_list:
                                f.write('{}\n'.format(item))
                        break
            dates_list += date_list
            print('{}-{}...done'.format(year, n))
        with open('{}_{}'.format(dates[0], dates[-1]), 'w') as fa:
            for item in dates_list:
                fa.write('{}\n'.format(item))
        return dates, dates_list

    def sln_multi_dates(self, dates):
        return

    def get_id(self, dates):
        id_list = []
        if dates:
            with open('dl_date_list', 'w') as dl:
                for _ in dates:
                    dl.write('{}\n'.format(_))
            with open('{}_{}'.format(dates[0], dates[-1])) as f1:
                id_list += f1.read().splitlines()
        else:
            print('No date file!')
        return id_list


class Downloader:

    def download(self, url, id_list):
        download_folder = 'Konachan.' + re.sub('[-]', '.', url.split('%3A')[-1])  # 创建下载文件夹
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        print('start downloading...')
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 '
                                 'Firefox/67.0'}
        proxy_url = {'http': 'http://127.0.0.1:7890'}
        for i in tqdm(id_list):
            url = 'https://konachan.com/post/show/{}'.format(i)  # 图片页面的链接
            page = requests.get(url, headers=headers, proxies=proxy_url)
            tree = html.fromstring(page.content)
            if tree.xpath('//*[@id="png"]/@href'):  # 从图片页面获得原图片文件元素xpath
                source = tree.xpath('//*[@id="png"]/@href')  # 图片页面没有png格式, 更换xpath
            else:
                source = tree.xpath('//*[@id="highres"]/@href')
            file_name = source[0].split('/')[-1]  # 从原图片地址的最后一段中获得图片描述的部分
            name = urllib.parse.unquote(file_name)  # 将其中的url转码为对应字符作为下载的文件名
            name_modify = re.sub('[*:?/|<>"]', '_', name)
            data = requests.get(source[0], headers=headers, proxies=proxy_url)
            with open(os.path.join(download_folder, name_modify), "wb") as file:  # 保存文件
                file.write(data.content)
            time.sleep(2)
        print('Download Succeed')
        return

    def sln_download(self, id_list):
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
        driver = webdriver.Chrome(chrome_options=chrome_options)
        for _ in tqdm(id_list):
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
        return


def syspath():
    path = os.getcwd().split('\\')
    path = '\\'.join(path[:3])
    path = path + '\\Downloads'
    return path
