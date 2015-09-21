from django.utils.translation import ugettext as _

APPT_LOCATIONS = (
    ('home', 'At home'),
    ('work', 'At work'),
    ('clinic', 'At clinic'),
    ('OTHER', 'Other location'),
)


APPT_GRADING = (
    ('firm', 'Firm appointment'),
    ('weak', 'Possible appointment'),
    ('guess', 'Estimated by RA'),
)

CONTACT_TYPE = (
    ('direct', 'Direct contact with participant'),
    ('indirect', 'Contact with person other than participant'),
    ('no_contact', 'No contact made'),
)

REFERRAL_APPT_COMMENTS = (
    ("N/A", "not applicable"),
    ("conflict", "have another commitment"),
    ("prefer_other_facility", "prefer another health facility than the local clinic"),
    ("prefer_other_date", "prefer to come on my own convenient time"),
    ("undecided_thinking", "have to think about it"),
    ("undecided_accepting_status", "need time to accept my HIV status"),
    ("have_other_anc_appt", "have already registered with ANC and have another appointment"),
    ("personal_reasons", "personal reasons"),
)

REFERRAL_CODES = (
    ('pending', '<data collection in progress>'),
    ('TST-CD4', 'POS any, need CD4 testing'),
    ('TST-HIV', 'HIV test'),
    ('MASA-CC', 'Known POS, MASA continued care'),
    ('MASA-DF', 'Known POS, MASA defaulter (was on ART)'),
    ('SMC-NEG', 'SMC (uncircumcised, hiv neg)'),
    ('SMC?NEG', 'SMC (Unknown circumcision status, hiv neg'),
    ('SMC-UNK', 'SMC (uncircumcised, hiv result not known)'),
    ('SMC?UNK', 'SMC (Unknown circumcision status, hiv result not known)'),
    ('NEG!-PR', 'NEG today, Pregnant'),
    ('POS!-PR', 'POS today, Pregnant'),
    ('UNK?-PR', 'HIV UNKNOWN, Pregnant'),
    ('POS#-AN', 'Known POS, Pregnant, on ART (ANC)'),
    ('POS#-PR', 'Known POS, Pregnant, not on ART'),
    ('POS!-HI', 'POS today, not on ART, high CD4)'),
    ('POS!-LO', 'POS today, not on ART, low CD4)'),
    ('POS#-HI', 'Known POS, not on ART, high CD4)'),
    ('POS#-LO', 'Known POS, not on ART, low CD4)'),
)

VISIT_INFO_SOURCE = [
    ('subject', '1. Subject'),
    ('other_member', '2. Other household member'),
    ('OTHER', '9. Other'),
]

VISIT_REASON = [
    ('consent', '1. Consent and Survey with subject'),
    ('absent', '2. Absentee'),
    ('undecided', '3. Undecided (with subject)'),
    ('refuse', '4. Refusal (with subject)'),
]


VISIT_UNSCHEDULED_REASON = (
    ('Routine oncology', _('Routine oncology clinic visit (i.e. planned chemo, follow-up)')),
    ('Ill oncology', _('Ill oncology clinic visit')),
    ('Patient called', _('Patient called to come for visit')),
    ('OTHER', _('Other, specify:')),
)


RELATIONSHIP_TYPE = (
    ('Longterm partner', _('Longterm partner (>2 years) or spouse')),
    ('Boyfriend/Girlfriend', _('Boyfriend/Girlfriend')),
    ('Casual', _('Casual (known) partner')),
    ('One time partner', _('One time partner (previously unknown)')),
    ('Commercial sex worker', _('Commercial sex worker')),
    ('Other, specify', _('Other, specify')),
)


MAIN_PARTNER_RESIDENCY = (
    ('In this community', _('In this community')),
    ('On farm/cattle post', _('On farm/cattle post')),
    ('Outside this community', _('Outside this community')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


SEX_REGULARITY = (
    ('All of the time', _('All of the time')),
    ('Sometimes', _('Sometimes')),
    ('Never', _('Never')),
)


INTERCOURSE_TYPE = (
    ('Vaginal', _('Vaginal sex')),
    ('Anal', _('Anal sex')),
    ('Both', _('Both vaginal and anal sex')),
)


#   CE001
MOBILITY = (
    ('no problems', _('I have no problems in walking about')),
    ('slight problems', _('I have slight problems in walking about')),
    ('moderate problems', _('I have moderate problems in walking about')),
    ('severe problems', _('I have severe problems in walking about')),
    ('unable to walk', _('I am unable to walk about')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


SELF_CARE = (
    ('no problems', _('I have no problems washing or dressing myself')),
    ('slight problems', _('I have slight problems washing or dressing myself')),
    ('moderate problems', _('I have moderate problems washing or dressing myself')),
    ('severe problems', _('I have severe problems washing or dressing myself')),
    ('unable to wash', _('I am unable to wash or dress myself')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


ACTIVITIES = (
    ('no problems', _('I have no problems doing my usual activities')),
    ('slight problems', _('I have slight problems doing my usual activities')),
    ('moderate problems', _('I have moderate problems doing my usual activities')),
    ('severe problems', _('I have severe problems doing my usual activities')),
    ('unable to', _('I am unable to do my usual activities')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


PAIN = (
    ('no pain', _('I have no pain or discomfort')),
    ('slight pain', _('I have slight pain or discomfort')),
    ('moderate pain', _('I have moderate pain or discomfort')),
    ('severe pain', _('I have severe pain or discomfort')),
    ('extreme pain', _('I have extreme pain or discomfort')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


ANXIETY = (
    ('not anxious', _('I am not anxious or depressed')),
    ('slightly anxious', _('I am slightly anxious or depressed')),
    ('moderately anxious', _('I am moderately anxious or depressed')),
    ('severely anxious', _('I am severely anxious or depressed')),
    ('extremely anxious', _('I am extremely anxious or depressed')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


CARE_FACILITIES = (
    ('Government Clinic/Post', _('Government Primary Health Clinic/Post')),
    ('Chemist/Pharmacy', _('Chemist/Pharmacy')),
    ('Hospital Outpatient Department', _('Hospital Outpatient Department (including government and private)')),
    ('Private Doctor', _('Private Doctor')),
    ('Traditional or Faith Healer', _('Traditional or Faith Healer')),
    ('No visit in past 3 months', _('No visit in past 3 months')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


CARE_REASON = (
    ('HIV-related care', _('HIV-related care, including TB and other opportunistic infections')),
    ('Pregnancy', _('Pregnancy-related care, including delivery')),
    ('Injuries', _('Injuries or accidents')),
    ('Chronic disease', _('Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness')),
    ('Other', _('Other')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
    ('None', _('None')),
)


TRAVEL_HOURS = (
    ('None', _('None')),
    ('Under 0.5 hour', _('Under 0.5 hour')),
    ('0.5 to under 1 hour', _('0.5 to under 1 hour')),
    ('1 to under 2 hours', _('1 to under 2 hours')),
    ('2 to under 3 hours', _('2 to under 3 hours')),
    ('More than 3 hours', _('More than 3 hours')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


NO_MEDICALCARE_REASON = (
    ('not thinking about HIV care', _('I am not thinking about HIV related medical/clinical '
                                      'care at this time')),
    ('I am not ready to start', _('HIV related medical/clinical care for my HIV infection '
                                  'is important to me but I am not ready to start it yet')),
    ('not yet tried to find a doctor', _('I have thought about starting HIV related medical/'
                                         'clinical care but have not yet tried to find a doctor or clinic')),
    ('not yet tried to make an appointment', _('I have found a doctor or clinic for HIV related '
                                               'medical/clinical care but have not yet tried to '
                                               'make an appointment')),
    ('no been successful yet', _('I have tried to obtain HIV related medical/clinical care from '
                                 'a doctor or clinic but have not been successful yet')),
    ('I have an appointment for HIV care', _('I have an appointment for HIV related medical/'
                                             'clinical care for my HIV infection but have not been for it yet')),
    ('don\'t know where to go', _('I don\'t know where to go for HIV related medical/clinical care')),
    ('I do not have the money', _('I do not have the money for HIV related medical/clinical care')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


HEALTH_CARE_PLACE = (
    ('None', _('None')),
    ('Government dispensary', _('Government dispensary')),
    ('Government health center', _('Government health center')),
    ('Government hospital', _('Government hospital')),
    ('Christian/mission health center', _('Christian/mission health center')),
    ('Islamic health center', _('Islamic health center')),
    ('Private health center for all illnesses', _('Private health center for all illnesses')),
    ('Private health center for HIV/AIDS', _('Private health center for HIV/AIDS')),
    ('Mobile services', _('Mobile services')),
    ('Plantation health center', _('Plantation health center')),
    ('NGO clinic', _('NGO clinic')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


CARE_REGULARITY = (
    ('0 times', _('0 times')),
    ('1 time', _('1 time')),
    ('2 times', _('2 times')),
    ('3 times', _('3 times')),
    ('4 times', _('4 times')),
    ('5 times', _('5 times')),
    ('6-10 times', _('6-10 times')),
    ('More than 10 times', _('More than 10 times')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


DOCTOR_VISITS = (
    ('always', _('All of the time (always)')),
    ('almost always', _('Most of the time (almost always)')),
    ('sometimes', _('Some of the time (sometimes)')),
    ('rarely', _('Almost none of the time (rarely)')),
    ('never', _('None of the time (never)')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


JOB_TYPE = (
    ('piece job', _('Occassional or Casual employment (piece job)')),
    ('seasonal', _('Seasonal employment')),
    ('full-time', _('Formal wage employment (full-time)')),
    ('part-time', _('Formal wage employment (part-time)')),
    ('agric', _('Self-employed in agriculture')),
    ('self full-time', _('Self-employed making money, full time')),
    ('self part-time', _('Self-employed making money, part time')),
    ('OTHER', _('Other')),
)


OCCUPATION = (
    ('Farmer', _('Farmer (own land)')),
    ('Farm worker', _('Farm worker (work on employers land)')),
    ('Domestic Worker', _('Domestic Worker')),
    ('Tavern/Bar/Entertainment', _('Work at Tavern/Bar/Entertainment Venue')),
    ('Mining', _('Mining')),
    ('Tourism', _('Tourism/game parks')),
    ('Informal vendors', _('Informal vendors')),
    ('Commercial sex work', _('Commercial sex work')),
    ('Transport (e.g., trucker)', _('Transport (e.g., trucker)')),
    ('Factory worker', _('Factory worker')),
    ('Informal vendors', _('Informal vendors')),
    ('Clerical and office work', _('Clerical and office work')),
    ('Small business/shop work', _('Small business/shop work')),
    ('Professional', _('Professional')),
    ('Fishing', _('Fishing')),
    ('Uniformed services', _('Uniformed services')),
    ('OTHER', _('Other, specify:')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)

REASON_UNEMPLOYED = (
    ('waiting', _('Waiting to continue agricultural work')),
    ('unemployed- looking', _('Unemployed (looking for work)')),
    ('unemployed- waiting', _('Unemployed (waiting to start new work)')),
    ('unable to work', _('Unable to work (permanently sick or injured)')),
    ('student', _('Student/ Apprentice/ Volunteer')),
    ('housewife', _('Housewife/ Homemaker (not looking for work)')),
    ('retired', _('Retired')),
    ('OTHER', _('Other')),
    ('not looking', _('Not looking for work')),
)


EMPLOYMENT_INFO = (
    ('government sector', _('Yes, In the government sector')),
    ('private sector', _('Yes, in the private sector')),
    ('self-employed working on my own', _('Yes, self-employed working on my own')),
    ('self-employed with own employees', _('Yes, self-employed with own employees')),
    ('not working', _('No, not working')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)

JOB_DESCRIPTION = (
    ('farmer', _('Farmer (own land)')),
    ('farm work', _('Farm work on employers land')),
    ('domestic', _('Domestic worker')),
    ('bar/hotel', _('Work in bar/ hotel/ guest house')),
    ('fishing', _('Fishing')),
    ('mining', _('Mining')),
    ('shop', _('Working in shop')),
    ('selling', _('Informal selling')),
    ('sexworker', _('Commercial sex work')),
    ('transport', _('Transport (trucker/ taxi driver)')),
    ('factory', _('Factory worker')),
    ('guard', _('Guard (security company)')),
    ('police', _('Police/ Soldier')),
    ('office', _('Clerical and office work')),
    ('govt worker', _('Government worker')),
    ('teacher', _('Teacher')),
    ('hcw', _('Health care worker')),
    ('Other', _('Other professional')),
    ('OTHER', _('Other')),
)

MONTHLY_INCOME = (
    ('None', _('No income')),
    ('1-199 pula', _('1-199 pula')),
    ('200-499 pula', _('200-499 pula')),
    ('500-999 pula', _('500-999 pula')),
    ('1000-4999 pula', _('1000-4999 pula')),
    ('5000-10,000 pula', _('5000-10,000 pula')),
    ('More than 10,000 pula', _('More than 10,000 pula')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)

SALARY = (
    ('Fixed salary', _('Fixed salary')),
    ('Paid daily', _('Paid daily')),
    ('Paid hourly', _('Paid hourly')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)

HOUSEHOLD_INCOME = (
    ('None', _('None')),
    ('1-200 pula', _('1-200 pula')),
    ('200-499 pula', _('200-499 pula')),
    ('500-999 pula', _('500-999 pula')),
    ('1000-4999 pula', _('1000-4999 pula')),
    ('5000-10,000 pula', _('5000-10,000 pula')),
    ('10,0000-20,000 pula', _('10,0000-20,000 pula')),
    ('More than 20,000 pula', _('More than 20,000 pula')),
    ('I am not sure', _('I am not sure')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)

OTHER_OCCUPATION = (
    ('None', _('None')),
    ('Studying', _('Studying')),
    ('Doing housework', _('Doing housework')),
    ('Looking for work', _('Looking for work')),
    ('Doing nothing (not looking for paid work)', _('Doing nothing (not looking for paid work)')),
    ('Retired/old age', _('Retired/old age')),
    ('Pregnant or recently pregnant', _('Pregnant or recently pregnant')),
    ('Sick or injured', _('Sick or injured')),
    ('OTHER', _('Other, specify:')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


HIV_DOC_TYPE = (
    ('Tebelopele', 'Tebelopele'),
    ('Lab result form', 'Lab result form'),
    ('ART Prescription', 'ART Prescription'),
    ('PMTCT Prescription', 'PMTCT Prescription'),
    ('Record of CD4 count', 'Record of CD4 count'),
    ('OTHER', 'Other OPD card or ANC card documentation'),
)

GRANT_TYPE = (
    ('Child support ', _('Child support ')),
    ('Old age pension', _('Old age pension')),
    ('Foster care', _('Foster care')),
    ('Disability', _('Disability (disability dependency)')),
    ('OTHER', _('Other, specify:')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


FLOORING_TYPE = (
    ('Dirt/earth', _('Dirt/earth ')),
    ('Wood, plank', _('Wood, plank')),
    ('Parquet/lino', _('Parquet/lino')),
    ('Cement', _('Cement')),
    ('Tile flooring', _('Tile flooring')),
    ('OTHER', _('Other, specify:')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


WATER_SOURCE = (
    ('Communal tap', _('Communal tap')),
    ('Standpipe/tap within plot', _('Standpipe/tap within plot')),
    ('Piped indoors', _('Piped indoors')),
    ('Borehore', _('Borehole')),
    ('Protected well', _('Protected well')),
    ('Unprotected/shallow well', _('Unprotected/shallow well')),
    ('River /dam/lake/pan', _('River /dam/lake/pan')),
    ('Bowser/tanker', _('Bowser/tanker')),
    ('OTHER', _('Other, specify (including unknown):')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


ENERGY_SOURCE = (
    ('Charcoal/wood', _('Charcoal/wood')),
    ('Paraffin', _('Paraffin')),
    ('Gas', _('Gas')),
    ('Electricity (mains)', _('Electricity (mains)')),
    ('Electricity (solar)', _('Electricity (solar)')),
    ('No cooking done', _('No cooking done')),
    ('OTHER', _('Other, specify:')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


TOILET_FACILITY = (
    ('Pit latrine within plot', _('Pit latrine within plot')),
    ('Flush toilet within plot', _('Flush toilet within plot')),
    ('Neighbour\'s flush toilet', _('Neighbour\'s flush toilet')),
    ('Neighbour\'s pit latrine', _('Neighbour''s pit latrine')),
    ('Communal flush toilet', _('Communal flush toilet')),
    ('Communal pit latrine', _('Communal pit latrine')),
    ('Pail bucket latrine', _('Pail bucket latrine')),
    ('Bush', _('Bush')),
    ('River or other body of water', _('River or other body of water')),
    ('OTHER', _('Other, specify:')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


SMALLER_MEALS = (
    ('Never', _('Never')),
    ('Rarely', _('Rarely')),
    ('Sometimes', _('Sometimes')),
    ('Often', _('Often')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
)


ENROLMENT_REASON = (
    ('CD4 < 50', _('Most recent (within past 3 months) CD4 < 50')),
    ('CD4 50-100', _('Most recent (within past 3 months) CD4 50-100')),
    ('AIDS opportunistic infection/condition', _('Current AIDS opportunistic infection/condition')),
)


OPPORTUNISTIC_ILLNESSES = (
    ('Tuberculosis', _('Tuberculosis')),
    ('Wasting', _('Wasting')),
    ('Cryptococcosis', _('Cryptococcosis')),
    ('severe bacterial pneumonia', _('Recurrent severe bacterial pneumonia')),
    ('Esophageal candidiasis', _('Esophageal candidiasis')),
    ('Pneumocystis pneumonia', _('Pneumocystis pneumonia')),
    ('Kaposi\'s sarcoma', _('Kaposi\'s sarcoma')),
    ('Cervical cancer', _('Cervical cancer')),
    ('Non-Hodgkin\'s lymphoma', _('Non-Hodgkin\'s lymphoma')),
    ('Other, record', _('Other, record')),
    ('No current AIDS opportunistic illness', _('No current AIDS opportunistic illness')),
)


REFERRAL_REASONS = (
    ('receive', _('Referred to receive HIV result in clinic')),
    ('test', _('Referred to test in clinic')),
    ('protocol', _('Referred as per protocol')),
)

RELATION = (
    ('spouse', _('spouse')),
    ('parent', _('parent')),
    ('sibling', _('sibling')),
    ('child', _('child')),
    ('aunt/uncle', _('aunt/uncle')),
    ('cousin', _('cousin')),
    ('partner', _('partner/boyfriend/girlfriend')),
    ('OTHER', _('Other, specify')),
)


YES_NO_RECORD_REFUSAL = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('Don\'t want to answer', _('Don\'t want to answer')),
    ('record refusal', _('Participant does not want to provide record')),
)

STI_DX = (
    ('wasting', 'Severe weight loss (wasting) - more than 10% of body weight'),
    ('diarrhoea', 'Unexplained diarrhoea for one month'),
    ('yeast infection', 'Yeast infection of mouth or oesophagus'),
    ('pneumonia', 'Severe pneumonia or meningitis or sepsis'),
    ('PCP', 'PCP (Pneumocystis pneumonia)'),
    ('herpes', 'Herpes infection for more than one month'),
    ('OTHER', 'Other'),
)

CHOICES_FROM_BCPPLIST = (
    ('Improved hygiene', _('Improved hygiene')),
    ('Reduced risk of HIV', _('Reduced risk of HIV')),
    ('Reduced risk of std', _('Reduced risk of other sexually transmitted diseases')),
    ('Reduced risk of cancer', _('Reduced risk of cancer')),
    ('heart_disease', _('Heart Disease or Stroke')),
    ('cancer', _('Cancer')),
    ('tb', _('Tuberculosis')),
    ('other_serious_infection', _('Other serious infection')),
    ('Radio', _('Radio')),
    ('TV', _('TV')),
    ('Landline telephone', _('Landline telephone')),
    ('Cell phone', _('Cell phone')),
    ('Computer', _('Computer')),
    ('Access to internet', _('Access to internet')),
    ('Refrigerator', _('Refrigerator')),
    ('Condoms, consistent use (male or female)', _('Condoms, consistent use (male or female)')),
    ('Injectable contraceptive', _('Injectable contraceptive')),
    ('Oral contraceptive', _('Oral contraceptive')),
    ('IUD', _('IUD')),
    ('Diaphragm or cervical cap', _('Diaphragm or cervical cap')),
    ('hythm or menstrual cycle timing', _('Rhythm or menstrual cycle timing')),
    ('Withdrawal', _('Withdrawal')),
    ('Myocardial infarction (heart attack)', _('Myocardial infarction (heart attack)')),
    ('Congestive cardiac failure', _('Congestive cardiac failure')),
    ('Stroke (cerebrovascular accident, CVA)', _('Stroke (cerebrovascular accident, CVA)')),
    ('Partner or spouse', _('Partner or spouse')),
    ('Siblings', _('Siblings')),
    ('Alone', _('Alone')),
    ('Extended family', _('Extended family')),
    ('Traditional, faith, or religious healer/doctor', _('Traditional, faith, or religious healer/doctor')),
    ('Pharmacy', _('Pharmacy')),
    ('ublic or government health facility or clinic', _('Public or government health facility or clinic')),
    ('Private health facility or clinic', _('Private health facility or clinic')),
    ('Community health worker', _('Community health worker')),
    ('Water', _('Water')),
    ('Sewer (sanitation)', _('Sewer (sanitation)')),
    ('Housing', _('Housing')),
    ('Roads', _('Roads')),
    ('Malaria', _('Malaria')),
    ('HIV/AIDS', _('HIV/AIDS')),
    ('Schools', _('Schools')),
    ('Unemployment', _('Unemployment')),
    ('In this community', _('In this community')),
    ('Outside community', _('Outside community')),
    ('Farm within', _('Farm within this community')),
    ('Farm outside this community', _('Farm outside this community')),
    ('cattlepost within', _('Cattle post within this community')),
    ('cattlepost outside', _('Cattle post outside this community')),
    ('Motor vehicle (car,truck,taxi, etc)', _('Motor vehicle (car,truck,taxi, etc)')),
    ('Tractor', _('Tractor')),
    ('Bicycle', _('Bicycle')),
    ('Motorcycle/scooter', _('Motorcycle/scooter')),
    ('Donkey or cow cart', _('Donkey or cow cart')),
    ('Donkey/horses', _('Donkey/horses')),
)

COUNSELING_SITE = (
    ('IN_HOME', 'In home'),
    ('MOBILE', 'Mobile Unit'),
    ('TENT', 'Tent'),
    ('CLINIC', 'Clinic'),
)
