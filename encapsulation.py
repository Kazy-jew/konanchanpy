from crawler import Downloader, Page_ID
from archive import Archive
from calendar import Calendar, syspath
import os

current = Calendar()
year = current.year


class DL_Core:
    def sln_core(self, id_list, dates):
        while id_list:
            Downloader().sln_download(id_list)
            id_list = Archive().check(dates)
        Archive().move(dates)
        for _ in dates:
            os.remove('./{}-{}'.format(year, _))
        os.remove('./{}_{}'.format(dates[0], dates[-1]))


class DL_Process:
    def bulk_dl(self):
        dates = current.date_input()
        print(dates)
        Page_ID().multi_dates(dates)
        id_list = Page_ID().get_id(dates)
        DL_Core().sln_core(id_list, dates)

    def chk_dl(self):
        with open('./dl_date_list', 'r') as r:
            dates = r.read().splitlines()
        print(dates)
        id_list = Archive().check(dates)
        DL_Core().sln_core(id_list, dates)