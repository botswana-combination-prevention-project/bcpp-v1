# choices
""" Try to keep this in alphabetical order """


ABSENTEE_STATUS = (
    ('ABSENT', 'Absent'),
    ('NOT_ABSENT', 'No longer absent'),    
)
    
ART_STATUS = (
    ('ON', 'Yes, ON ART'),
    ('STOPPED', 'No, stopped ART'),
    ('NAIVE', 'No, have never taken ART'),
)

ART_STATUS_CONFIRM = (
    ( 'OPD', '1. Show OPD/IDCC card' ),
    ( 'Pills','2. Show Pills'),
    ( 'Pic', '3. Identify Pictorial'),
)

DOB_ESTIMATE = (
    ('-', 'Yes'),
    ('D', 'No, estimated the Day'),            
    ('MD', 'No, estimated Month and Day'),
    ('YMD', 'No, estimated Year, Month and Day'),            
)
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

HOUSEHOLD_VISIT_STATUS = (
    (1, 'Complete'),
    (2, 'No'),
)

LOCATIONS = (
    ('CLINIC', 'Clinic'),
    ('HOUSEHOLD', 'Household'),
)

POS_NEG = (
    ('POS', 'Positive'),
    ('NEG', 'Negative'),
    ('IND', 'Indeterminate'),
)

POS_NEG_ANY = (
    ('POS', 'Positive'),
    ('NEG', 'Negative'),
    ('ANY', 'Any'),
)

POS_NEG_ACU = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
    ('Possible Acute', 'Possible Acute'),
    ('Indeterminate', 'Indeterminate'),
)    

POS_NEG_NOTESTED = (
    ('POS', 'Positive'),
    ('NEG', 'Negative'),
    ('NEVER', 'Never tested for HIV'),
)

REFUSAL_STATUS = (
    ('REFUSED','Refused'),
    ('NOT_REFUSED','No longer refusing'),    
)    

RESULT_OPTIONS = (
    ('A','A'),
    ('B','B'),
    ('C','C'),
    ('D','D'),
    ('E','E'),
)   

WILL_DECL = (
    ('WILLING', 'Willing'),
    ('DELINED', 'Delined'),
)

YES_NO = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)


YES_NO_NA = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('N/A', 'Not applicable'),    
)
YES_NO_UNSURE = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not Sure', 'Not Sure'),
)




