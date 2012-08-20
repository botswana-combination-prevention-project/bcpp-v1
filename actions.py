from models import ContentTypeMap
#from django.contrib.contenttypes.management import update_all_contenttypes


def pop_and_sync(modeladmin, request, queryset):
    #update_all_contenttypes()
    ContentTypeMap.objects.populate()
    ContentTypeMap.objects.sync()
pop_and_sync.short_description = "Re-populate and sync content type"
