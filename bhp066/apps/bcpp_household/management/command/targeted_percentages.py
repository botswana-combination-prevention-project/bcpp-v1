from edc.map.classes import site_mappers
site_mappers.autodiscover()
mapper = site_mappers.get_registry('ranaka')()

pid_file  = open('ranaka.txt', 'r')
lines = pid_file.readlines()
line_list = lines[0].split('\r')


for item in items:
	if item.plot_identifier in line_list:
		item.selected=1
		item.save()

