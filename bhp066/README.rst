v1.2.6

you will also need to add in bhp066 (where manage.py is) three repos

git clone git@gitserver:edc
git clone git@gitserver:edc_templates templates
git clone git@gitserver:lis

project structure is

apps: BCPP specific apps
edc: core edc apps and code
lis: core lis apps and code that edc and bcpp use
locale:
media:
static: (be sure to run collectstatic)
templates: (clone of edc_templates)
keys:
bhp066: settings and urls

-erik

check prermissions and content_type are aligned. Anything that prints is bad.

for p in Permission.objects.all():
    if unicode(p.content_type.model) not in p.codename.split('_'): 
        print p.content_type.model, p.codename