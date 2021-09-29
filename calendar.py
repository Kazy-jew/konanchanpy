from datetime import date, timedelta

class Calendar:
    def __init__(self):
        self.year = 2021

    def set_year(self, year):
        self.year = year

    def date_range(self, start, end):
        delta = end - start
        date_lis = []
        for i in range(delta.days+1):
            date_lis.append(str(start+timedelta(days=i)))
        date_lis = [_.replace('{}-'.format(self.year), '') for _ in date_lis]
        return date_lis

    def date_input(self):
        date_in = [x for x in input('please input a date range(month, date, date): ').split()]
        self.date_list = self.date_range(date(int('{}'.format(self.year)), int('{:>2}'.format(date_in[0])), int('{:>2}'.format(date_in[1]))),
                          date(int('{}'.format(self.year)), int('{:>2}'.format(date_in[0])), int('{:>2}'.format(date_in[2]))))
        print(self.date_list)
        return self.date_list
