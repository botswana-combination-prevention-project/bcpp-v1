from datetime import datetime
from django.db import models
from bhp_content_type_map.models import ContentTypeMap
from bhp_entry.managers import BaseEntryBucketManager


class AdditionalEntryBucketManager(BaseEntryBucketManager):

    def is_keyed(self):
        """ Confirms if model instance exists / is_keyed. """
        model = models.get_model(
                        self.content_type_map.content_type.app_label,
                        self.content_type_map.content_type.model)
        if model.objects.filter(registered_subject=self.registered_subject).exists():
            is_keyed = True
        else:
            is_keyed = False
        return is_keyed

    def get_entries_for(self, **kwargs):
        """Returns a queryset of AdditionalEntryBucket objects for the given subject."""
        entry_category = kwargs.get("entry_category", 'clinic')
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError("Manager get_entries_for expected registered_subject. Got None.")
        additional_entry_bucket = super(AdditionalEntryBucketManager, self).filter(
                                            registered_subject=registered_subject,
                                            entry__entry_category__iexact=entry_category,
                                            ).order_by('entry__entry_order')
        return additional_entry_bucket

    def add_for(self, registered_subject, model, qset):
        """Checks that the form has been keyed already."""
        if not model.objects.filter(qset):
            content_type_map = ContentTypeMap.objects.get(name=model._meta.verbose_name)
            if not super(AdditionalEntryBucketManager, self).filter(
                    registered_subject=registered_subject,
                    content_type_map=content_type_map).exists():
                # add to bucket
                super(AdditionalEntryBucketManager, self).create(
                    registered_subject=registered_subject,
                    content_type_map=content_type_map,
                    current_entry_title=model._meta.verbose_name,
                    fill_datetime=datetime.today(),
                    due_datetime=datetime.today())

    def update_status(self, **kwargs):
        """Updates status."""
        self.registered_subject = kwargs.get('registered_subject')
        if not self.registered_subject:
            raise AttributeError('AdditionalEntryBucketManager.update_status requires \'registered_subject\'. Got None')
        self.set_content_type_map(**kwargs)
        action = kwargs.get('action', 'add_change')
        comment = kwargs.get('comment', '----')
        if self.content_type_map and self.registered_subject:
            if super(AdditionalEntryBucketManager, self).filter(registered_subject=self.registered_subject,
                                                                content_type_map=self.content_type_map):
                additional_bucket_entry = super(AdditionalEntryBucketManager, self).get(registered_subject=self.registered_subject,
                                                                                        content_type_map=self.content_type_map)
                status = self.get_status(
                    action=action,
                    report_datetime=self.report_datetime,
                    current_status=additional_bucket_entry.entry_status,
                    entry_comment=comment
                    )

                additional_bucket_entry.report_datetime = status['report_datetime']
                additional_bucket_entry.entry_status = status['action']
                additional_bucket_entry.entry_comment = status['entry_comment']
                additional_bucket_entry.close_datetime = status['close_datetime']
                additional_bucket_entry.modified = datetime.today()
                additional_bucket_entry.save()
