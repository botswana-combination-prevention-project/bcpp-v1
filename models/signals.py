from django.db.models.signals import post_save, pre_save, post_delete
from django.db.models import get_app, get_models
from django.dispatch import receiver
from consent_catalogue import ConsentCatalogue
from attached_model import AttachedModel
from bhp_content_type_map.models import ContentTypeMap
from bhp_consent.models import BaseConsent, BaseConsentedUuidModel


@receiver(pre_save, weak=False, dispatch_uid='is_consented_instance_on_pre_save')
def is_consented_instance_on_pre_save(sender, instance, **kwargs):
    if isinstance(instance, BaseConsentedUuidModel):
        if instance.get_requires_consent():
            if not instance.is_consented_for_instance():
                raise TypeError('Data may not be collected. Model {0} is not covered by a valid consent for this subject.'.format(instance._meta.object_name))
            instance.validate_versioned_fields()


@receiver(post_save, weak=False, dispatch_uid='add_models_to_catalogue')
def add_models_to_catalogue(sender, instance, **kwargs):
    """Automatically adds all models to the AttachedModel model if ConsentCatalogue.add_for_app is a valid app_label."""
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


@receiver(post_save, weak=False, dispatch_uid='update_consent_history')
def update_consent_history(sender, instance, raw, created, using, **kwargs):
    """Updates the consent history model with this instance if such model exists."""
    if isinstance(instance, BaseConsent):
        instance.update_consent_history(created, using)


@receiver(post_delete, weak=False, dispatch_uid='delete_consent_history')
def delete_consent_history(sender, instance, using, **kwargs):
    """Updates the consent history model with this instance if such model exists."""
    if isinstance(instance, BaseConsent):
        instance.delete_consent_history(instance._meta.app_label, instance._meta.object_name, instance.pk, using)
