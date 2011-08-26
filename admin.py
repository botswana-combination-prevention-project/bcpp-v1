from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from models import DxCode

admin.site.register(DxCode)
