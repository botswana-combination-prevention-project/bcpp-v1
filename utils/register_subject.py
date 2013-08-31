# from datetime import date, timedelta, datetime
# from bhp_registration.models import SubjectIdentifierAuditTrail
# from bhp_variables.models import StudySpecific
# from bhp_registration.models import RegisteredSubject
# 
# 
# def RegisterSubject (**kwargs):
# 
#     if kwargs.get('identifier') is None:
#         raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'identifier\'. Got None.')
# 
#     if kwargs.get('consent_pk') is None:
#         raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'consent_pk\'. Got None.')
# 
#     if kwargs.get('first_name') is None:
#         raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'first_name\'. Got None.')
# 
#     if kwargs.get('initials') is None:
#         raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'initials\'. Got None.')
# 
#     if kwargs.get('subject_type') is None:
#         raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'subject_type\'. Got None.')
# 
#     if kwargs.get('user') is None:
#         raise TypeError( 'bhp_registration.RegisterSubject expects a value for \'user\'. Got None.')
# 
# 
#     registered_subject = RegisteredSubject(
#         subject_identifier = kwargs.get('identifier'),
#         registration_datetime=datetime.now(),
#         subject_type = kwargs.get('subject_type').upper(),
#         user_created=kwargs.get('user'),
#         created=datetime.now(),
#         subject_consent_id=kwargs.get('consent_pk'),
#         first_name=kwargs.get('first_name'),
#         initials=kwargs.get('initials').upper(),
#         registration_status='registered',
#         relative_identifier = kwargs.get('relative_identifier'),
#         )
# 
#     registered_subject.save()
# 
#     return registered_subject
