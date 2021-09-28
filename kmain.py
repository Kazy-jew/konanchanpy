# from datetime import date
from konachan_crawler import *
from count_page import *
import os

year = '2021'


def selenium_core(id_list, dates):
    while id_list:
        sln_download(id_list)
        id_list = check(dates)
    move(dates)
    for _ in dates:
        os.remove('./{}-{}'.format(year, _))
    os.remove('./{}_{}'.format(dates[0], dates[-1]))


def bulk_dl():
    d = [x for x in input('please input a date range(month, date, date): ').split()]
    bdate = date_list(date(int('{}'.format(year)), int('{:>2}'.format(d[0])), int('{:>2}'.format(d[1]))),
                      date(int('{}'.format(year)), int('{:>2}'.format(d[0])), int('{:>2}'.format(d[2]))))
    print(bdate)
    multi_pages(bdate)
    img_list = get_id(bdate)
    selenium_core(img_list, bdate)


def chk_dl():
    with open('./dl_date_list', 'r') as r:
        chkdate = r.read().splitlines()
    print(chkdate)
    lis = check(chkdate)
    selenium_core(lis, chkdate)


print('   Welcome to Konachan Downloader ! ')
print('--------------------------------------')
print('|************************************|')
print('|*** 1.download   2.the remaining ***|')
print('|*** 3. exit                      ***|')
print('|************************************|')
print('¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯')
while True:
    choice = input('select operation: ')
    if choice == '1':
        bulk_dl()
    elif choice == '2':
        chk_dl()
    elif choice == '3':
        exit()
    else:
        print('invalid input')

