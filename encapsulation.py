from crawler import Downloader, Page_ID
from archive import Archive
from calendar import Calendar
import os

year = Calendar().year


class DL_Core:
    def sln_core(self, id_list, dates):
        while id_list:
            Downloader().sln_download(id_list)
            id_list = Archive().check(dates)
        Archive().move(dates)
        for _ in dates:
            os.remove('./{}-{}'.format(year, _))
        os.remove('./{}_{}'.format(dates[0], dates[-1]))

    def sln_tags(self, id_list, tags):
        while id_list:
            Downloader().sln_download(id_list)
            id_list = Archive().checktag(tags)
        Archive.move(tags)
        list_dir = os.listdir('./')
        page_list_name = [x for x in list_dir if 'Konachan.tag({}).p'.format(tags) in x]
        for i in page_list_name:
            os.remove('./{}'.format(i))
        os.remove('./Konachan.tags({})'.format(tags))


class DL_Process:
    def bulk_dl(self):
        dates = Calendar().date_input()
        Page_ID().multi_dates(dates)
        id_list = Page_ID().get_id(dates)
        DL_Core().sln_core(id_list, dates)

    def chk_dl(self, tags=None):
        if tags is None:
            with open('./dl_date_list', 'r') as r:
                dates = r.read().splitlines()
            print(dates)
            id_list = Archive().check(dates)
            DL_Core().sln_core(id_list, dates)
        else:
            id_list = Archive().checktag(tags)
            DL_Core().sln_tags(id_list, tags)


    def tag_dl(self):
        tags_url = input('please paste url here')
        tags = tags_url.split('tags=')[-1]
        id_list = Page_ID().custom_url(tags_url)
        DL_Core().sln_tags(id_list, tags)



class Print_Welcome:
    def konachan(self):
        print('    Welcome to Konachan Downloader ! ')
        print('---------------------------------------')
        print('|*************************************|')
        print('|*** 1.download    2.the remaining ***|')
        print('|*** 3.custom tags 4.exit  ***********|')
        print('|*************************************|')
        print('¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯')

    def yande_re(self):
        pass

    def minitokyo(self):
        pass