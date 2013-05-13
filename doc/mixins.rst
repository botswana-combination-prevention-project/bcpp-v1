Mixins
=======

Using the OffStudyMixin
+++++++++++++++++++++++

The off study mixin provides methods required to manage a subject's off-study status.

    1. Make a subclass of :class:`OffStudyMixin` in your app/module. The subclass should reside in the :mod:`models` module.::
    
        from bhp_off_study.mixins import OffStudyMixin
        from maternal_off_study import MaternalOffStudy
        
        
        class MaternalOffStudyMixin(OffStudyMixin):
        
            def get_off_study_cls(self):
                return MaternalOffStudy

    2. Ensure that all models in the module have access to the mixin methods by adding to the model class declaration 
       (preferably on base classes). For example, 
        
        Consent::
           
            from bhp_botswana.models import BaseBwConsent
            from maternal_off_study_mixin import MaternalOffStudyMixin


            class BaseMaternalConsent(MaternalOffStudyMixin, BaseBwConsent):
            
                class Meta:
                    abstract = True

        Registration::

            from bhp_registration.models import BaseRegistrationModel
            from mpepu_maternal.managers import MaternalRegistrationModelManager
            from maternal_off_study_mixin import MaternalOffStudyMixin
            
            
            class BaseMaternalRegistrationModel(MaternalOffStudyMixin, BaseRegistrationModel):
            
                objects = MaternalRegistrationModelManager()
            
                class Meta:
                    abstract = True
                    
        Scheduled models that inheret from BaseConsentedUuidModel::

            from bhp_consent.models import BaseConsentedUuidModel
            from maternal_off_study_mixin import MaternalOffStudyMixin
            
            
            class MaternalBaseUuidModel(MaternalOffStudyMixin, BaseConsentedUuidModel):
            
                """ Base model for all maternal models """
            
                class Meta:
                    abstract = True

    3. Run tests to ensure that all models use the mixin and :mod:`bhp_consent` has access to the required model methods. For example::
    
            def test_off_study_mixin(self):
                print 'check each model has off study methods from mixin'
                app = get_app('mpepu_infant')
                for model in get_models(app):
                    if 'Audit' not in model._meta.object_name and 'OffStudy' not in model._meta.object_name:
                        print model._meta.object_name
                        self.assertTrue('get_off_study_cls' in dir(model), 'Method \'get_off_study_cls\' not found on model {0}'.format(model._meta.object_name))
                        self.assertTrue('is_off_study' in dir(model), 'Method \'is_off_study\' not found on model {0}'.format(model._meta.object_name))
                        self.assertTrue('get_report_datetime' in dir(model), 'Method \'get_report_datetime\' not found on model {0}'.format(model._meta.object_name))
                        self.assertTrue('get_subject_identifier' in dir(model), 'Method \'get_subject_identifier\' not found on model {0}'.format(model._meta.object_name))
         
        

Classes
+++++++

.. automodule:: bhp_off_study.mixins

.. autoclass:: OffStudyMixin
    :members:
    :show-inheritance:
    :private-members: