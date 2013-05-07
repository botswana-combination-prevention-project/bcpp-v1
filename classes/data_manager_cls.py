from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured


class DataManagerCls(object):
    def prepare(self):
        if not Group.objects.filter(name='data_manager').exists():
            Group.objects.create(name='data_manager')
        if not Group.objects.filter(name='action_manager').exists():
            Group.objects.create(name='action_manager')

    def check(self):
        if not Group.objects.filter(name='data_manager').exists():
            raise ImproperlyConfigured('Group \'data_manager\' does not exist. Add data_manager.prepare() to your urls.py before admin.autodiscover(). See bhp_data_manager.')
        if not Group.objects.filter(name='action_manager').exists():
            raise ImproperlyConfigured('Group \'action_manager\' does not exist. Add data_manager.prepare() to your urls.py before admin.autodiscover(). See bhp_data_manager.')
        return True

data_manager = DataManagerCls()
