import requests
from lxml import html
#
# url = 'https://www.youtube.com/watch?v=Jn09UdSb3aA'
# page = requests.get(url)
# tree = html.fromstring(page.content)
# target = tree.xpath('/html/body/script[1]/text()')
with open('list.txt', 'r') as f:
    reh = f.read().splitlines()
print(reh)
rehh = [x for x in reh if x!='']
with open('list1.txt', 'w') as f1:
    for _ in rehh:
        f1.write('{}\n'.format(_))
