import os, shutil
from calendar import Calendar
from crawler import syspath

path = syspath()
year = Calendar().year

class Archive:
    def check(self, dates):
        list1 = os.listdir(path)
        list2 = []
        list3 = []
        for w in list1:
            if w.startswith('Konachan.com'):
                list2.append(w.split()[2])
        if len(dates) > 1:
            with open('{}_{}'.format(dates[0], dates[-1]), 'r') as r:
                list3 += r.read().splitlines()
        elif len(dates) == 1:
            with open('{}-{}'.format(year, dates[0]), 'r') as r:
                list3 += r.read().splitlines()
        diff = list(set(list3) - set(list2))
        with open('undownloaded', 'w') as f:
            for _ in diff:
                f.write('{}\n'.format(_))
        return diff

    def move(self, dates):
        list1 = os.listdir(path)
        list2 = []
        for i in list1:
            if i.startswith('Konachan.com'):
                list2.append(i)
        for m in dates:
            with open('{}-{}'.format(year, m)) as r:
                pairli = r.read().splitlines()
            folder = 'Konachan.{}.{}'.format(m.split('-')[0], m.split('-')[1])
            if not os.path.exists(os.path.join(path, folder)):
                os.makedirs(os.path.join(path, folder))
            for j in list2:
                name_id = j.split(' ')[2]
                if name_id in pairli:
                    shutil.move(os.path.join(path, j), os.path.join(path, folder))