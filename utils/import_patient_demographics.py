"""
from bhp_lab_core.utils import import_patient_demographics    
import_patient_demographics('/home/django/ctu_patients.csv')
"""    
def import_patient_demographics(csv_filename):
    import csv
    import time
    from datetime import datetime, timedelta
    from lab_patient.models import SimpleConsent, Patient
    from bhp_research_protocol.models import Protocol, Site
    
    f = open(csv_filename, 'rb')

    """
    format of csv file is:
    SUBJECT_IDENTIFIER , PROTOCOL_NAME, SITE_CODE, CONSENT_STARTDATE, DOB, DOB_ESTIMATED,  GENDER,  STUDY_STATUS,  
    CONSENT_ENDDATE
    
    ALL DATES in YYYY-MM-DD format
    PROTOCOL_NAME is a valid BHP number (BHP032, etc)
    SITE_CODE is a valid BHP site code
    DOB_ESTIMATED is Y/N. If Y (yes), the estimation is assumed MD if the DOB is YYYY-07-01 and D if YYYY-MM-01 
    GENDER is M/F
    STUDY_STATUS is ON/OFF
    """

    reader = csv.reader(f)
    
    SUBJECT_IDENTIFIER = 0     
    PROTOCOL_NAME=1
    SITE_CODE=2
    CONSENT_STARTDATE=3
    DOB=4
    DOB_ESTIMATED=5
    GENDER=6
    STUDY_STATUS=7
    CONSENT_ENDDATE=8
    i = 0     
    for row in reader:
        i +=1
        if i == 1 or row[DOB]=='':
            pass
        else:
            
            time_format = "%Y-%m-%d"
            dob=datetime.fromtimestamp(time.mktime(time.strptime(row[DOB], time_format)))

            subject_identifier = row[SUBJECT_IDENTIFIER]
            gender = row[GENDER]
            
            oSite = Site.objects.get(site_identifier__exact=row[SITE_CODE])
            protocol_name = row[PROTOCOL_NAME]
            if protocol_name == '1077HS':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP049')
            elif protocol_name == 'A5208':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP017')
            elif protocol_name == 'A5221':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP033')    
            elif protocol_name == 'A5234':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP053')
            elif protocol_name == 'A5253':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP046')    
            elif protocol_name == 'P1026S':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP050')    
            elif protocol_name == 'P1041':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP023')    
            elif protocol_name == 'P1066':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP035')    
            elif protocol_name == 'P1072':
                oProtocol = Protocol.objects.get(protocol_identifier__iexact='BHP040')    
            else:
                raise TypeError('unknown protocol %s' % protocol_name)

            consent_startdate=datetime.fromtimestamp(time.mktime(time.strptime(row[CONSENT_STARTDATE], time_format)))

            if not row[CONSENT_ENDDATE]:
                consent_enddate = None
            else:
                consent_enddate=datetime.fromtimestamp(time.mktime(time.strptime(row[CONSENT_ENDDATE], time_format)))
                
                
            if row[DOB_ESTIMATED] == 'Y':
                is_dob_estimated = 'MD'
            else:    
                is_dob_estimated = '-'

            # create a simple consent
            #raise TypeError(consent_startdate)
            oSimpleConsent = SimpleConsent.objects.create(
                protocol = oProtocol,
                consent_site = oSite,
                consent_startdate = consent_startdate,
                consent_enddate = consent_enddate,
                may_store_samples = 'YES'
                )
            oSimpleConsent.save()

            # update or create a patient
            if not Patient.objects.filter(subject_identifier__iexact=subject_identifier):
                # create
                
                oPatient = Patient.objects.create(
                    subject_identifier=subject_identifier.lower(),
                    gender = gender, 
                    dob = dob,
                    is_dob_estimated = is_dob_estimated,
                    )    
                oPatient.save()        
                oPatient.simple_consent.add(oSimpleConsent)
                oPatient.save()                        
            else:        
                # update
                oPatient = Patient.objects.get(subject_identifier__iexact=subject_identifier)
                oPatient.gender = gender
                oPatient.dob = dob
                oPatient.is_dob_estimated = is_dob_estimated
                oPatient.simple_consent.add(oSimpleConsent)
                oPatient.save()        


if __name__ == "__main__":
    
    import sys,os
    sys.path.append('/home/django/source/')
    sys.path.append('/home/django/source/bhplab/')
    os.environ['DJANGO_SETTINGS_MODULE'] ='bhplab.settings'
    from django.core.management import setup_environ
    from bhplab import settings

    setup_environ(settings)
    
    import_patient_demographics('/home/django/ctu_patients.csv')

    sys.exit (0)                         



