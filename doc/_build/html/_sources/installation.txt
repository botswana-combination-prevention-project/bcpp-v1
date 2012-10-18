Installation
============

Checkout the latest version of :mod:`lab_tracker` into your test environment project folder::

    svn co http://192.168.1.50/svn/lab_tracker


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
        'lab_tracker',
        ...
        )

Add the following to your :file:`settings.py`::

    tracker.autodiscover()

For each subject type you wish to track, create a subclass of :class:`History`::

    class HivHistory(History):
    
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
                history_model, created = HistoryModel.objects.get_or_create(subject_identifier=subject_identifier,
                                                                            test_key=test_key,
                                                                            test_code='RELISA',
                                                                            value_datetime=subject_hiv_result.subject_visit.report_datetime,
                                                                            defaults=defaults)
                if not created:
                    if subject_hiv_result.subject_hiv_result_option.result_option:
                        history_model.result = self.value_map[subject_hiv_result.subject_hiv_result_option.result_option]
                        history_model.save()
            return None
       
Add a :file:`tracker.py` file to the module::

    from lab_tracker.classes import tracker
    from classes import HivHistory
    from models import SubjectHivResult
    
    
    tracker.register(SubjectHivResult, HivHistory) 
    
A model may have a method like this::

    def hiv_status(self):
        """Updates and returns hiv history using the HivHistory object and
        model but does not update the hsm self.hiv_history attr.

        To update all::
            >>> for rs in RegisteredSubject.objects.filter(subject_identifier__isnull=False):
            >>>     for hsm in HouseholdStructureMember.objects.filter(registered_subject=rs, hiv_history__isnull=True):
            >>>     # print hsm
            >>>     hsm.save()
        """
        retval = ''
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                hiv_history = HivHistory()
                retval = hiv_history.get_as_string(self.registered_subject.subject_identifier)
        return retval