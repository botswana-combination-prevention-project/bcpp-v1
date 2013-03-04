from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models import ContentTypeMap
from actions import pop_and_sync


class ContentTypeMapAdmin(MyModelAdmin):
    list_display = ('name', 'content_type', 'id', 'model', 'app_label')
    search_fields = ('name', 'app_label', 'model')
    list_filter = ('app_label',)
    actions = [pop_and_sync]
admin.site.register(ContentTypeMap, ContentTypeMapAdmin)
