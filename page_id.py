'''
 返回指定日期的图片id列表
 return the id list of images by (a) specified date(s)
'''
import requests
from lxml import html
import selenium
import os
from calendar import Calendar

class Page_ID:
    def multi_pages(self, mdate):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/92.0.4515.131 Safari/537.36'}
        proxy_url = {'http': 'http://127.0.0.1:7890'}
        # id list of date range
        multi_date_list = []
        year = Calendar().year
        for n in mdate:
            # id list of a date
            id_list = []
            if os.path.exists('{}-{}'.format(year, n)):
                print('list {} already downloaded...'.format(n))
                with open('{}-{}'.format(year, n), 'r') as r:
                    id_list += r.read().splitlines()
            else:
                for i in range(1, 24):
                    url = 'https://konachan.com/post?page={}&tags=date%3A{}-{}'.format(i, year, n)
                    page_ = requests.get(url, headers=headers, proxies=proxy_url)
                    tree = html.fromstring(page_.content)
                    mark_tag = tree.xpath('//*[@id="post-list"]/div[3]/div[4]/p/text()')
                    if not mark_tag:
                        id_list += tree.xpath('//*[@id="post-list-posts"]/li/@id')
                    elif mark_tag == ['Nobody here but us chickens!']:
                        id_list = [w.replace('p', '') for w in id_list]
                        with open('{}'.format(url.split('%3A')[-1]), 'w') as f:
                            for item in id_list:
                                f.write('{}\n'.format(item))
                        break
            multi_date_list += id_list
            print('{}-{}...done'.format((year, n)))
        with open('{}_{}'.format(mdate[0], mdate[-1]), 'w') as fa:
            for item in multi_date_list:
                fa.write('{}\n'.format(item))
        return mdate, multi_date_list

    def selenium_multi(self, sdate):
        return