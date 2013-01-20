
Models
======  

#Base Classes for Subject Models
#++++++++++++++++++++++++++++++++
#
#.. autoclass:: base_consented_uuid_model.BaseConsentedUuidModel
#    :members:   


Consent Base Classes
++++++++++++++++++++

.. autoclass:: base_consent.BaseConsent
    :members:    

.. autoclass:: base_consent_update.BaseConsentUpdate
    :members:  

Consent Catalogue
+++++++++++++++++

Each consent type is catalogued by name, version and time period. For each catalogued
consent, the models it covers are listed. When a subject_instance is saved, ModelForm :func:`clean` and
Model :func:`save` check that the model class of the subject instance is named in the list of
models covered by the subject's consent. 

.. autoclass:: ConsentCatalogue
    :members:  

.. autoclass:: AttachedModel
    :members:  
    
Other
+++++

.. autoclass:: Consent
    :members:  
