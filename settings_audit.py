from django.db import models


def get_subject_identifier(obj):

    """Used by AuditTrail to update an add track field _audit_subject_identifier.

    If the path to the subject identifier is not obvious, add a get_visit() method to
    the model that returns the visit instance:

        def get_visit(self):
            return self.maternal_lab_del_dx.maternal_visit

    """

    subject_identifier = ''

    try:
        if [fld for fld in obj._meta.fields if fld.name == 'subject_identifier']:
            subject_identifier = obj.subject_identifier
        elif [fld for fld in obj._meta.fields if fld.name == 'subject_visit']:
            subject_identifier = eval('obj.subject_visit.appointment.registered_subject.subject_identifier')
        elif [fld for fld in obj._meta.fields if fld.name == 'appointment']:
            subject_identifier = obj.appointment.registered_subject.subject_identifier
        elif [fld for fld in obj._meta.fields if fld.name == 'registered_subject']:
            subject_identifier = obj.registered_subject.subject_identifier
        elif 'get_visit' in dir(obj):
            subject_identifier = obj.get_visit().appointment.registered_subject.subject_identifier
        elif 'get_subject_identifier' in dir(obj):
            subject_identifier = obj.get_subject_identifier()
        else:
            #raise TypeError('AuditTrail cannot find the subject_identifier. Perhaps add a get_visit() or get_subject_identifier() method to the model')
            pass
    except:
        pass    
    return subject_identifier

# Populate the fields that every Audit model in this app will use.
GLOBAL_TRACK_FIELDS = (
    ('_audit_subject_identifier', models.CharField(max_length=50, null=True), get_subject_identifier),
    #('_audit_comment', models.CharField(max_length=250, null=True, blank=True), ''),
    )

