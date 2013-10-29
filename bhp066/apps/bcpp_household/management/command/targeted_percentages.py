from edc.map.classes import site_mappers
site_mappers.autodiscover()
mapper = site_mappers.get_registry('digawana')()
pid_file  = open('digawana.txt', 'r')
lines = pid_file.readlines()
line_list = []
for li in lines:
	line_list.append(li[:-1])

items = Plot.objects.all()


for item in items:
	if item.plot_identifier in line_list:
		item.selected=1
		item.save()
		
		
pid_file2 = open('digawana_25.txt', 'r')
lines2 = pid_file2.readlines()

l1 = []

for lq in lines2:
	l1.append(lq[:-1])


l2 = []

for i in l1:
	if not i in line_list:
		l2.append(i)
		
		
items = Plot.objects.all()
		
for item in items:
	if item.plot_identifier in l2:
		item.selected=2
		item.save()