Installation
============

Checkout the latest version of :mod:`bhp_lab_tracker` into your test environment project folder::

    svn co http://192.168.1.50/svn/bhp_lab_tracker


Add :mod:`lab_tracker` to your project ''settings'' file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'django.contrib.admindocs',
        'django_extensions',
        'audit_trail',
        'bhp_base_model',
        'bhp_common',
        'bhp_lab_tracker',
        ...
        )

Add the following to your :file:`settings.py`::

    tracker.autodiscover()

For each subject type you wish to track, create a subclass of :class:`History`::

    class HivTracker(LabTracker):
    
        def get_value_map_prep(self):
            SubjectHivResultOption = get_model('mochudi_subject', 'subjecthivresultoption')
            value_map = {}
            for opt in SubjectHivResultOption.objects.all():
                if opt.result_word.lower() == 'negative':
                    result = 'NEG'
                elif opt.result_word.lower() == 'positive':
                    result = 'POS'
                elif opt.result_word.lower() == 'possible acute':
                    result = 'ACUTE'
                elif opt.result_word.lower() == 'indeterminate':
                    result = 'IND'
                else:
                    result = 'UNK'
                value_map.update({opt.result_option: result})
            return value_map
    
        def get_prep(self):
            """ Returns a list of format [test_code, test_key] where test_codes are those in :class:`ResultItem` that have HIV results."""
            return (['ELISA', 'RELISA', 'DNAPCR'], 'HIV')
    
        def update_prep(self, subject_identifier, test_key):
            SubjectHivResult = get_model('mochudi_subject', 'subjecthivresult')
            for subject_hiv_result in SubjectHivResult.objects.filter(subject_visit__appointment__registered_subject__subject_identifier=subject_identifier):
                defaults = {'value': self.value_map[subject_hiv_result.subject_hiv_result_option.result_option]}
                history_model, created = HistoryModel.objects.get_or_create(
                    subject_identifier=subject_identifier,
                    test_key=test_key,
                    test_code='RELISA',
                    value_datetime=subject_hiv_result.subject_visit.report_datetime,
                    defaults=defaults)
                if not created:
                    if subject_hiv_result.subject_hiv_result_option.result_option:
                        history_model.result = self.value_map[subject_hiv_result.subject_hiv_result_option.result_option]
                        history_model.save()
            return None
       
Add a :file:`lab_tracker.py` file to the module. 

Examples of :file:`lab_tracker.py`
++++++++++++++++++++++++++++++++++

1. Configure longitudinal tracking of a value in lab_clinic_api.ResultItem only::

    from bhp_lab_tracker.classes import lab_tracker
    from bhp_lab_tracker.classes import HivLabTracker
    
    
    class InfantHivLabTracker(HivLabTracker):
        pass
    lab_tracker.register(InfantHivLabTracker)

2. Configure longitudinal tracking of a value that includes values from local models as well as 
   lab_clinic_api.ResultItem::

    from bhp_lab_tracker.classes import lab_tracker
    from bhp_lab_tracker.classes import HivLabTracker
    from models import MaternalEligibilityPost, MaternalEligibilityAnte
    
    
    class MaternalHivLabTracker(HivLabTracker):
        models = (
            (MaternalEligibilityPost, 'is_hiv_positive', 'registration_datetime'),
            (MaternalEligibilityAnte, 'is_hiv_positive', 'registration_datetime')
            )
    lab_tracker.register(MaternalHivLabTracker)


   In this case, local models have been registered. Note the following:
      1. models are registered as a tuple of (class, value_attr, date_attr) where value_attr is the 
         field attribute name for the result value and date_attr is the datetime attribute for the 
         datetime of the result.
      2. This class is a subclass of :class:`HivLabTracker`. This class is predefined in :mod:`bhp_lab_tracker`
         where some additional required class attributes are already defined.