VISIT_INTERVAL_UNITS = (
    ('H', 'Hour'),
    ('D', 'Day'),
    ('M', 'Month'),
    ('Y', 'Year'),            
    )
    
   
    
TAG_TYPE = (
    ('REGISTRATION', 'Registration'),
    ('OTHER', 'Other'),    
)    

APPT_STATUS = (
    ('Scheduled', 'Scheduled'),
    ('Subject Seen', 'Subject Seen'),
    ('Cancelled', 'Cancelled'),        
    ) 
    
SUBJECT_TYPE = (
    ('ADULT','ADULT'),
    ('MOTHER','MOTHER'),
    ('INFANT','INFANT'),
    ('SUBJECT','SUBJECT'),
    ('INDEX','INDEX'),
    ('PARTNER','PARTNER'),                                                                                                                            
) 

VISIT_INFO_SOURCE = (
    ('participant', '1. Clinic visit with participant'),
    ('other_contact', '2. Other contact with participant'),
    ('other_doctor', '3. Contact with external health care provider/medical doctor'),
    ('family', '4. Contact with family or designated person who can provide information'),
    ('chart', '5. Hospital chart or other medical record'),
    ('OTHER', '9. Other'),
    )

VISIT_REASON = (
    ('scheduled', '1. Scheduled visit/contact'),
    ('missed', '2. Missed Scheduled visit'),
    ('unscheduled', '3. Unscheduled visit at which lab samples or data are being submitted'),
    ('lost', '4. Lost to follow-up'),
    ('death', '5. Death'),
)    
