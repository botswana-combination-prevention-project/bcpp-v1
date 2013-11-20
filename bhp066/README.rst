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

python manage.py update_visit_schedule_permissions comm_liaison_officer --app_label bcpp_household

python manage.py update_visit_schedule_permissions field_research_assistant --visit_codes all
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_subject --models subjectconsent
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_subject --models subjectvisit
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_subject --models subjectabsentee
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_subject --models subjectabsenteeentry
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_subject --models subjectrefusal
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_subject --models subjectundecided
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_subject --models subjectundecidedentry
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_household
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_household_member
python manage.py update_visit_schedule_permissions field_research_assistant --app_label bcpp_lab
python manage.py update_visit_schedule_permissions field_research_assistant --app_label appointment --models appointment

python manage.py update_visit_schedule_permissions clinic_research_assistant --visit_codes all
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_subject --models subjectconsent
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_subject --models subjectvisit
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_subject --models subjectabsentee
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_subject --models subjectabsenteeentry
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_subject --models subjectrefusal
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_subject --models subjectundecided
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_subject --models subjectundecidedentry
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_household
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_household_member
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label bcpp_lab
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label appointment --models appointment
python manage.py update_visit_schedule_permissions clinic_research_assistant --app_label lab_clinic_api 

python manage.py update_visit_schedule_permissions IT_assistant --visit_codes all
python manage.py update_visit_schedule_permissions IT_assistant --app_label bcpp_subject --models subjectconsent
python manage.py update_visit_schedule_permissions IT_assistant --app_label bcpp_subject --models subjectvisit
python manage.py update_visit_schedule_permissions IT_assistant --app_label bcpp_household
python manage.py update_visit_schedule_permissions IT_assistant --app_label bcpp_household_member
python manage.py update_visit_schedule_permissions IT_assistant --app_label bcpp_lab
python manage.py update_visit_schedule_permissions IT_assistant --app_label sync
python manage.py update_visit_schedule_permissions IT_assistant --app_label tastypie 
python manage.py update_visit_schedule_permissions IT_assistant --app_label appointment --models appointment
python manage.py update_visit_schedule_permissions IT_assistant --app_label lab_clinic_api 
python manage.py update_visit_schedule_permissions IT_assistant --app_label auth
 
python manage.py update_visit_schedule_permissions lab_assistant --visit_codes all
python manage.py update_visit_schedule_permissions lab_assistant --app_label bcpp_lab
python manage.py update_visit_schedule_permissions lab_assistant --app_label bcpp_inspector
python manage.py update_visit_schedule_permissions lab_assistant --app_label appointment --models appointment
python manage.py update_visit_schedule_permissions lab_assistant --app_label lab_clinic_api 
python manage.py update_visit_schedule_permissions lab_assistant --app_label bcpp_subject --models subjectvisit
python manage.py update_visit_schedule_permissions lab_assistant --visit_codes all
python manage.py update_visit_schedule_permissions lab_assistant --app_label sync
python manage.py update_visit_schedule_permissions lab_assistant --app_label tastypie
python manage.py update_visit_schedule_permissions lab_assistant --app_label bcpp_subject --models subjectconsent

python manage.py update_visit_schedule_permissions field_supervisor --visit_codes all
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_subject --models subjectconsent
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_subject --models subjectabsentee
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_subject --models subjectabsenteeentry
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_subject --models subjectrefusal
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_subject --models subjectundecided
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_subject --models subjectundecidedentry
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_household
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_household_member
python manage.py update_visit_schedule_permissions field_supervisor --app_label bcpp_la
python manage.py update_visit_schedule_permissions field_supervisor --app_label lab_clinic_api 
python manage.py update_visit_schedule_permissions field_supervisor --app_label appointment --models appointment

python manage.py update_visit_schedule_permissions IT_admin --visit_codes all
python manage.py update_visit_schedule_permissions IT_admin --app_label bcpp_subject --models subjectconsent
python manage.py update_visit_schedule_permissions IT_admin --app_label bcpp_subject --models subjectvisit
python manage.py update_visit_schedule_permissions IT_admin --app_label bcpp_household
python manage.py update_visit_schedule_permissions IT_admin --app_label bcpp_household_member
python manage.py update_visit_schedule_permissions IT_admin --app_label bcpp_lab
python manage.py update_visit_schedule_permissions IT_admin --app_label appointment --models appointment
python manage.py update_visit_schedule_permissions IT_admin --app_label lab_clinic_api 
python manage.py update_visit_schedule_permissions IT_admin --app_label auth
 