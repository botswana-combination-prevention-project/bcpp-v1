from bhp_subject.managers import BaseSubjectManager


class RegisteredSubjectManager(BaseSubjectManager):

    pass

#     def update_with(self, instance, attrname='subject_identifier', **kwargs):
#         """ Use an instance, usually a consent, to update registered subject.
# 
#         ..note:: IS NO LONGER USED FOR CONSENTS, see bhp_base_subject.models.base_subject.post_save_get_or_create_registered_subject().
# 
#         Assume all required fields attributes are included in the instance.
#         Additional fields may be passed as kwargs.
# 
#         To avoid creating a new registered subject record/instance for a subject that
#         already exists, access the registered_subject attribute on 'instance', if it exists
#         and is not null. Otherwise, create an new registered_subject
# 
#         It is the responsibility of the calling model (usually a consent) to help
#         with instance.registered_subject.
#         """
#         using = kwargs.get('using', None)
#         #print 'update_with' + using
#         # attrname is one of the following "registered subject" unique field attributes
#         valid_attrnames = ('subject_identifier', 'identity')
#         registered_subject = None
#         if attrname not in valid_attrnames:
#             raise TypeError('Attribute must represent a unique field such as {0}. Got {1}.'.format(', '.join(valid_attrnames), attrname))
#         try:
#             # if the registered subject already exists and is part of 'instance', use it
#             registered_subject = getattr(instance, 'registered_subject')
#         except:
#             # use attrname and its value from 'instance' to search for the registered_subject, if it exists
#             value = getattr(instance, attrname)
#             if super(RegisteredSubjectManager, self).using(using).filter(**{attrname: value}):
#                 registered_subject = super(RegisteredSubjectManager, self).using(using).get(**{attrname: value})
#         if registered_subject:
#             # update an existing registered_subject
#             if not registered_subject.subject_identifier:
#                 registered_subject.subject_identifier = getattr(instance, attrname)
#             registered_subject.user_modified = instance.user_modified
#             registered_subject.modified = datetime.today()
#             registered_subject.first_name = instance.first_name
#             registered_subject.last_name = instance.last_name
#             registered_subject.initials = instance.initials
#             registered_subject.gender = instance.gender
#             registered_subject.study_site = instance.study_site
#             registered_subject.identity = instance.identity
#             registered_subject.identity_type = instance.identity_type
#             registered_subject.dob = instance.dob
#             registered_subject.is_dob_estimated = instance.is_dob_estimated
#             registered_subject.may_store_samples = instance.may_store_samples
#             registered_subject.subject_type = instance.get_subject_type()
#         else:
#             # create a new registered subject
#             registered_subject = super(RegisteredSubjectManager, self).using(using).create(
#                 # relative_identifier = kwargs.get('relative_identifier', None),
#                 # subject_identifier = kwargs.get('subject_identifier'),
#                 subject_consent_id=None,
#                 registration_status=kwargs.get('registration_status', None),
#                 registration_datetime=datetime.today(),
#                 subject_identifier=getattr(instance, attrname),
#                 user_created=instance.user_created,
#                 created=datetime.today(),
#                 first_name=instance.first_name,
#                 last_name=instance.last_name,
#                 initials=instance.initials,
#                 gender=instance.gender,
#                 study_site=instance.study_site,
#                 identity=instance.identity,
#                 identity_type=instance.identity_type,
#                 dob=instance.dob,
#                 is_dob_estimated=instance.is_dob_estimated,
#                 may_store_samples=instance.may_store_samples,
#                 subject_type=instance.get_subject_type(),
#                 )
#         # set values for any extra attributes, or overwrite the value from above
#         extra = False
#         for attr in kwargs:
#             if kwargs.get(attr):
#                 extra = True
#                 setattr(registered_subject, attr, kwargs.get(attr))
#         if extra:
#             registered_subject.save(using=using)
