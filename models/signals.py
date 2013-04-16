from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, weak=False, dispatch_uid='bhp_visit_prepare_appointments_on_post_save')
# def bhp_visit_prepare_appointments_on_post_save(sender, instance, **kwargs):
#     if 'registered_subject' in dir(instance):
#         instance.prepare_appointments()
