from django.contrib.admin.sites import AdminSite


class EdcSite(AdminSite):
    pass

site = EdcSite(name='edc_site')
