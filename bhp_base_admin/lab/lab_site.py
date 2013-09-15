from django.contrib.admin.sites import AdminSite


class LabSite(AdminSite):
    pass

site = LabSite(name='lab_site')
