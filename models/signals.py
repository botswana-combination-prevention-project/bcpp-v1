from django.db.models.signals import post_save
from django.db.models import get_app, get_models
from django.dispatch import receiver
from consent_catalogue import ConsentCatalogue
from attached_model import AttachedModel
from bhp_content_type_map.models import ContentTypeMap


@receiver(post_save, weak=False, dispatch_uid='add_models_to_catalogue')
def add_models_to_catalogue(sender, instance, **kwargs):
    if sender == ConsentCatalogue:
        if instance.add_for_app:
            try:
                app = get_app(instance.add_for_app)
            except:
                app = None
            if app:
                # sync content_type_map
                ContentTypeMap.objects.populate()
                ContentTypeMap.objects.sync()
                # add models to AttachedModel
                models = get_models(app)
                for model in models:
                    if 'consent' not in model._meta.object_name.lower() and 'audit' not in model._meta.object_name.lower():
                        if ContentTypeMap.objects.filter(model=model._meta.object_name.lower()):
                            content_type_map = ContentTypeMap.objects.get(model=model._meta.object_name.lower())
                            if not AttachedModel.objects.filter(consent_catalogue=instance, content_type_map=content_type_map).exists():
                                AttachedModel.objects.create(consent_catalogue=instance, content_type_map=content_type_map)
