from urllib import urlretrieve
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError

        
class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community>'
    help = 'Creates map images for all the items.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
    
        mapper_name = args[0]
        site_mappers.autodiscover()
        if not site_mappers.get_registry(mapper_name):
            raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
        else:
            m = site_mappers.get_registry(mapper_name)()
            
            #NOT YET COMPLETE: TODO
            
            
            items = m.get_item_model_cls().objects.filter(**{m.map_area_field_attr: mapper_name})
            idnt = m.get_identifier_field_attr()
            for item in items:
                name = item.m.get_identifier_field_attr()
                print name
                urls = ''
                folder = settings.MEDIA_ROOT
                print folder
#                 count = 0
#                 for src in urls:
#                     count += 1
#                     file_name = folder + name + '.jpg'
#                     urlretrieve(src, file_name)
#                     print str((count/float(len(urls)))*100) + ' percent done! only ' + str(len(urls) - count) + ' more pictures to download'
#                     sleep(5)