import os
list1 = []
for i in range(3, 9):
	with open('./2019-11-0{}'.format(i)) as p:
		list1 += p.read().splitlines()
print(len(list1))
with open ('./11-03_11-08', 'w') as q:
	for _ in list1:
		q.write('{}\n'.format(_))