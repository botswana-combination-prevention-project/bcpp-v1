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


permissions
1. clear the Permission model

python manage.py clear_permissions

2. edit out south in settings.py
3. run syncdb

python manage.py syncdb

4. do the following:

python manage.py update_visit_schedule_permissions field_research_assistant --visit_codes all
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_household
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_household_member
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_lab
python manage.py update_visit_schedule_permissions field_research_assistant --app_label appointment --models appointment

python manage.py update_visit_schedule_permissions clinic_research_assistant --visit_codes all
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_household
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_household_member
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_lab
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label appointment --models appointment

