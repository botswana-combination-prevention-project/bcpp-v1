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

CONFIRMED_SUSPECTED = (
    ('CONFIRMED', 'Confirmed'),
    ('SUSPECTED', 'Suspected'),
)    

DATE_ESTIMATED = (
    ('-', 'No'),
    ('D', 'Yes, estimated the Day'),            
    ('MD', 'Yes, estimated Month and Day'),
    ('YMD', 'Yes, estimated Year, Month and Day'),            
)

FEEDING = (
   ('BF', 'Breast Feed'),
   ('FF', 'Formula Feed'),   
)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

GENDER_UNDETERMINED = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U' , 'Undetermined'),
)

GRADE = (
    ('1', 'Grade 1'),
    ('2', 'Grade 2'),
    ('3', 'Grade 3'),        
    ('4', 'Grade 4'),
    ('5', 'Grade 5'),        
)

HOUSEHOLD_VISIT_STATUS = (
    (1, 'Complete'),
    (2, 'No'),
)

"""do not change without inspecting implication to check_omang_field() in utils.py"""
IDENTITY_TYPE = (
    ('OMANG', 'Omang'),
    ('DRIVERS', 'Driver\'s License'),
    ('PASSPORT', 'Passport'),
    ('OMANG_RCPT', 'Omang Receipt'),                    
    ('OTHER', 'Other'),                        
)

LOCATIONS = (
    ('CLINIC', 'Clinic'),
    ('HOUSEHOLD', 'Household'),
)

NORMAL_ABNORMAL =(
    ('NORMAL', 'Normal'),
    ('ABNORMAL', 'Abnormal'),
)

NORMAL_ABNORMAL_NOEXAM =(
    ('NORMAL', 'Normal'),
    ('ABNORMAL', 'Abnormal'),
    ('NO_EXAM', 'No Exam Performed'),
)

NORMAL_ABNORMAL_NOTEVALUATED =(
    ('NORMAL', 'Normal'),
    ('ABNORMAL', 'Abnormal'),
    ('NOT_EVAL', 'Not Evaluated'),
)

POS_NEG =(
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

ISSUE_STATUS = (
    ('NEW', 'New'),
    ('OPEN', 'Open'),
    ('STALLED', 'Stalled'),
    ('CLOSED', 'Closed'),                            
)

TIME_UNITS = (
    ('TODAY', 'Today'),
    ('DAYS', 'Days'),
    ('WEEKS', 'Weeks'),
    ('MONTHS', 'Months'),
    ('YEARS', 'Years'),    
)


WILL_DECL = (
    ('WILLING', 'Willing'),
    ('DELINED', 'Declined'),
)

YES_NO = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

YES_NO_NA_SPECIFY = (
    ('Yes', 'Yes, (Specify below)'),
    ('No', 'No'),
    ('N/A', 'Not applicable'),    
)

YES_NO_NA = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('N/A', 'Not applicable'),    
)

YES_NO_UNKNOWN =(
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Unknown', 'Unknown'),
)    

YES_NO_UNSURE = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not Sure', 'Not Sure'),
)

YES_NO_DONT_KNOW = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Dont_know', 'Do not Know'),
)

