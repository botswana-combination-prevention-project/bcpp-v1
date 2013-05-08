VISIT_UNSCHEDULED_REASON = (
    ('Routine oncology', 'Routine oncology clinic visit (i.e. planned chemo, follow-up)'),
    ('Ill oncology', 'Ill oncology clinic visit'),
    ('Patient called', 'Patient called to come for visit'),
    ('OTHER', 'Other, specify:'),
)


RELATIONSHIP_TYPE = (
    ('Longterm partner', 'Longterm partner (>2 years) or spouse'),
    ('Boyfriend/Girlfriend', 'Boyfriend/Girlfriend'),
    ('Casual', 'Casual (known) partner'),
    ('One time partner', 'One time partner (previously unknown)'),
    ('Commercial sex worker', 'Commercial sex worker'),
    ('Other, specify', 'Other, specify'), 
)


MAIN_PARTNER_RESIDENCY = (
    ('In this community', 'In this community'),
    ('On farm/cattle post', 'On farm/cattle post'),
    ('Outside this community', 'Outside this community'),
    ('Don\'t want to answer', 'Don\'t want to answer'),
)


SEX_REGULARITY = (
    ('All of the time', 'All of the time'),
    ('Sometimes', 'Sometimes'),
    ('Never', 'Never'),
)


INTERCOURSE_TYPE = (
    ('Vaginal', 'Vaginal sex'),
    ('Anal', 'Anal sex'),
    ('Both', 'Both vaginal and anal sex'),
)


#   CE001
MOBILITY = (
    ('no problems', 'I have no problems in walking about'),
    ('slight problems', 'I have slight problems in walking about'),
    ('moderate problems', 'I have moderate problems in walking about'),
    ('severe problems', 'I have severe problems in walking about'),
    ('unable to walk', 'I am unable to walk about'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


SELF_CARE = (
    ('no problems', 'I have no problems washing or dressing myself'),
    ('slight problems', 'I have slight problems washing or dressing myself'),
    ('moderate problems', 'I have moderate problems washing or dressing myself'),
    ('severe problems', 'I have severe problems washing or dressing myself'),
    ('unable to wash', 'I am unable to wash or dress myself'),
    ('Don\'t want to answer', 'Don\t want to answer'),
) 


ACTIVITIES = (
    ('no problems', 'I have no problems doing my usual activities'),
    ('slight problems', 'I have slight problems doing my usual activities'),
    ('moderate problems', 'I have moderate problems doing my usual activities'),
    ('severe problems', 'I have severe problems doing my usual activities'),
    ('unable to', 'I am unable to do my usual activities'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


PAIN = (
    ('no pain', 'I have no pain or discomfort'),
    ('slight pain', 'I have slight pain or discomfort'),
    ('moderate pain', 'I have moderate pain or discomfort'),
    ('severe pain', 'I have severe pain or discomfort'),
    ('extreme pain', 'I have extreme pain or discomfort'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


ANXIETY = (
    ('not anxious', 'I am not anxious or depressed'),
    ('slightly anxious', 'I am slightly anxious or depressed'),
    ('moderately anxious', 'I am moderately anxious or depressed'),
    ('severely anxious', 'I am severely anxious or depressed'),
    ('extremely anxious', 'I am extremely anxious or depressed'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


CARE_FACILITIES = (
    ('Government Clinic/Post', 'Government Primary Health Clinic/Post'),
    ('Chemist/Pharmacy', 'Chemist/Pharmacy'),
    ('Hospital Outpatient Department', 'Hospital Outpatient Department (including government and private)'),
    ('Private Doctor', 'Private Doctor'),
    ('Traditional or Faith Healer', 'Traditional or Faith Healer'),
    ('No visit in past 3 months', 'No visit in past 3 months'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


CARE_REASON = (
    ('HIV-related care', 'HIV-related care, including TB and other opportunistic infections'),
    ('Pregnancy', 'Pregnancy-related care, including delivery'),
    ('Injuries', 'Injuries or accidents'),
    ('Chronic disease', 'Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness'),
    ('Other', 'Other'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


TRAVEL_HOURS = (
    ('Under 0.5 hour', 'Under 0.5 hour'),
    ('0.5 to under 1 hour', '0.5 to under 1 hour'),
    ('1 to under 2 hours', '1 to under 2 hours'),
    ('2 to under 3 hours', '2 to under 3 hours'),
    ('More than 3 hours', 'More than 3 hours'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


NO_MEDICALCARE_REASON = (
    ('not thinking about HIV care', 'I am not thinking about HIV related medical/clinical care at this time'),
    ('I am not ready to start', 'HIV related medical/clinical care for my HIV infection is important to me but I am not ready to start it yet'),
    ('not yet tried to find a doctor', 'I have thought about starting HIV related medical/clinical care but have not yet tried to find a doctor or clinic'),
    ('not yet tried to make an appointment', 'I have found a doctor or clinic for HIV related medical/clinical care but have not yet tried to make an appointment'),
    ('no been successful yet', 'I have tried to obtain HIV related medical/clinical care from a doctor or clinic but have not been successful yet'),
    ('I have an appointment for HIV care', 'I have an appointment for HIV related medical/clinical care for my HIV infection but have not been for it yet'),
    ('don\'t know where to go', 'I don\'t know where to go for HIV related medical/clinical care'),
    ('I do not have the money', 'I do not have the money for HIV related medical/clinical care'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


HEALTH_CARE_PLACE = (
    ('Government dispensary', 'Government dispensary'),
    ('Government health center', 'Government health center'),
    ('Government hospital', 'Government hospital'),
    ('Christian/mission health center', 'Christian/mission health center'),
    ('Islamic health center', 'Islamic health center'),
    ('Private health center for all illnesses', 'Private health center for all illnesses'),
    ('Private health center for HIV/AIDS', 'Private health center for HIV/AIDS'),
    ('Mobile services', 'Mobile services'),
    ('Plantation health center', 'Plantation health center'),
    ('NGO clinic', 'NGO clinic'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


CARE_REGULARITY = (
    ('0 times', '0 times'),
    ('1 time', '1 time'),
    ('2 times', '2 times'),
    ('3 times', '3 times'),
    ('4 times', '4 times'),
    ('5 times', '5 times'),
    ('6-10 times', '6-10 times'),
    ('More than 10 times', 'More than 10 times'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)  


DOCTOR_VISITS = (
    ('always', 'All of the time (always)'),
    ('almost always', 'Most of the time (almost always)'),
    ('sometimes', 'Some of the time (sometimes)'),
    ('rarely', 'Almost none of the time (rarely)'),
    ('never', 'None of the time (never)'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


EMPLOYMENT_INFO = (
    ('government sector', 'Yes, In the government sector'),
    ('private sector', 'Yes, in the private sector'),
    ('self-employed working on my own', 'Yes, self-employed working on my own'),
    ('self-employed with own employees', 'Yes, self-employed with own employees'),
    ('not working', 'No, not working'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


OCCUPATION = (
    ('Farmer', 'Farmer (own land)'),
    ('Farm worker', 'Farm worker (work on employers land)'),
    ('Domestic Worker', 'Domestic Worker'),
    ('Tavern/Bar/Entertainment', 'Work at Tavern/Bar/Entertainment Venue'),
    ('Mining', 'Mining'),
    ('Tourism', 'Tourism/game parks'),
    ('Informal vendors', 'Informal vendors'),
    ('Commercial sex work', 'Commercial sex work'),
    ('Transport (e.g., trucker)', 'Transport (e.g., trucker)'),
    ('Factory worker', 'Factory worker'),
    ('Informal vendors', 'Informal vendors'),
    ('Clerical and office work', 'Clerical and office work'),
    ('Small business/shop work', 'Small business/shop work'),
    ('Professional', 'Professional'),
    ('Fishing', 'Fishing'),
    ('Uniformed services', 'Uniformed services'),
    ('OTHER', 'Other, specify:'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


MONTHLY_INCOME = (
    ('None', 'None'),
    ('1-200 pula', '1-200 pula'),
    ('200-499 pula', '200-499 pula'),
    ('500-999 pula', '500-999 pula'),
    ('1000-4999 pula', '1000-4999 pula'),
    ('5000-10,000 pula', '5000-10,000 pula'),
    ('More than 10,000 pula', 'More than 10,000 pula'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)

SALARY = (
    ('Fixed salary', 'Fixed salary'),
    ('Paid daily', 'Paid daily'),
    ('Paid hourly', 'Paid hourly'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)

HOUSEHOLD_INCOME = (
    ('None', 'None'),
    ('1-200 pula', '1-200 pula'),
    ('200-499 pula', '200-499 pula'),
    ('500-999 pula', '500-999 pula'),
    ('1000-4999 pula', '1000-4999 pula'),
    ('5000-10,000 pula', '5000-10,000 pula'),
    ('10,0000-20,000 pula', '10,0000-20,000 pula'),
    ('More than 20,000 pula', 'More than 20,000 pula'),
    ('I am not sure', 'I am not sure'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)

OTHER_OCCUPATION = (
    ('Studying', 'Studying'),
    ('Doing housework', 'Doing housework'),
    ('Looking for work', 'Looking for work'),
    ('Doing nothing (not looking for paid work)', 'Doing nothing (not looking for paid work)'),
    ('Retired/old age', 'Retired/old age'),
    ('Pregnant or recently pregnant', 'Pregnant or recently pregnant'),
    ('Sick or injured', 'Sick or injured'),
    ('OTHER', 'Other, specify:'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


GRANT_TYPE = (
    ('Child support ', 'Child support '),
    ('Old age pension', 'Old age pension'),
    ('Foster care', 'Foster care'),
    ('Disability', 'Disability (disability dependency)'),
    ('OTHER', 'Other, specify:'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


FLOORING_TYPE = (
    ('Dirt/earth', 'Dirt/earth '),
    ('Wood, plank', 'Wood, plank'),
    ('Parquet/lino', 'Parquet/lino'),
    ('Cement', 'Cement'),
    ('Tile flooring', 'Tile flooring'),
    ('OTHER', 'Other, specify:'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


WATER_SOURCE = (
    ('Communal tap', 'Communal tap'),
    ('Standpipe/tap within plot', 'Standpipe/tap within plot'),
    ('Piped indoors', 'Piped indoors'),
    ('Borehore', 'Borehole'),
    ('Protected well', 'Protected well'),
    ('Unprotected/shallow well', 'Unprotected/shallow well'),
    ('River /dam/lake/pan', 'River /dam/lake/pan'),
    ('Bowser/tanker', 'Bowser/tanker'),
    ('OTHER', 'Other, specify (including unknown):'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


ENERGY_SOURCE = (
    ('Charcoal/wood', 'Charcoal/wood'),
    ('Paraffin', 'Paraffin'),
    ('Gas', 'Gas'),
    ('Electricity (mains)', 'Electricity (mains)'),
    ('Electricity (solar)', 'Electricity (solar)'),
    ('No cooking done', 'No cooking done'),
    ('OTHER', 'Other, specify:'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


TOILET_FACILITY = (
    ('Pit latrine within plot', 'Pit latrine within plot'),
    ('Flush toilet within plot', 'Flush toilet within plot'),
    ('Neighbour\'s flush toilet', 'Neighbour\'s flush toilet'),
    ('Neighbour\'s pit latrine', 'Neighbour''s pit latrine'),
    ('Communal flush toilet', 'Communal flush toilet'),
    ('Communal pit latrine', 'Communal pit latrine'),
    ('Pail bucket latrine', 'Pail bucket latrine'),
    ('Bush', 'Bush'),
    ('River or other body of water', 'River or other body of water'),
    ('OTHER', 'Other, specify:'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)


SMALLER_MEALS = (
    ('Never', 'Never'),
    ('Rarely', 'Rarely'),
    ('Sometimes', 'Sometimes'),
    ('Often', 'Often'),
    ('Don\'t want to answer', 'Don\t want to answer'),
)

 
ENROLMENT_REASON = (
    ('CD4 < 50', 'Most recent (within past 3 months) CD4 < 50'),
    ('CD4 50-100', 'Most recent (within past 3 months) CD4 50-100'),
    ('AIDS opportunistic infection/condition', 'Current AIDS opportunistic infection/condition'),
)
 
 
OPPORTUNISTIC_ILLNESSES = (
    ('Tuberculosis', 'Tuberculosis'),
    ('Wasting', 'Wasting'),
    ('Cryptococcosis', 'Cryptococcosis'),
    ('severe bacterial pneumonia', 'Recurrent severe bacterial pneumonia'),
    ('Esophageal candidiasis', 'Esophageal candidiasis'),
    ('Pneumocystis pneumonia', 'Pneumocystis pneumonia'),
    ('Kaposi\'s sarcoma', 'Kaposi\'s sarcoma'),
    ('Cervical cancer', 'Cervical cancer'),
    ('Non-Hodgkin\'s lymphoma', 'Non-Hodgkin\'s lymphoma'),
    ('Other, record', 'Other, record'),
    ('No current AIDS opportunistic illness', 'No current AIDS opportunistic illness'),
)
 

NEXT_APPOINTMENT_SOURCE = (
    ('subject', 'Subject'), 
    ('household member', 'household member'), 
    ('hbc', 'HBC'), 
    ('other', 'Other')
)


ABSENTEE_STATUS = (
    ('ABSENT', 'Absent'),
    ('NOT_ABSENT', 'No longer absent'),
)


MOVED_REASON = (
    ('TRANSFER', 'Job Transfer'),
    ('MARRIAGE', 'Marriage'),
    ('INDEPENDENT', 'Independence'),
    ('OTHER', 'Other'),
)

PLACE_SUBJECT_MOVED = (
    ('IN_MOCHUDI', 'Within Mochudi'),
    ('OUT_MOCHUDI', 'Outside Mochudi'),
    ('IN_WARD', 'Within the Survey Ward'),
)


ABSENTEE_REASON = (
    (u'goes to school in mochudi and comes home daily', u'Schools in Mochudi, home daily'),
    (u'goes to school outside mochudi and comes home daily', u'Schools outside Mochudi, home daily'),
    (u'goes to school outside mochudi and comes home irregularly ', u'Schools outside Mochudi, home irregularly '),
    (u'goes to school outside mochudi and comes home monthly ', u'Schools outside Mochudi, home monthly '),
    (u'goes to school outside mochudi and comes home on weekends ', u'Schools outside Mochudi, home on weekends '),
    (u'gone visiting (relatives,holidays,weddings,funerals)', u'Gone visiting'),
    (u'stays at lands or cattlepost ', u'Stays at Lands/Cattlepost '),
    (u'stepped out(shops, errands etc) ', u'Stepped out (shops, errands, ) '),
    (u'works in mochudi and comes home daily', u'Works in Mochudi, home daily'),
    (u'works outside mochudi and comes home daily', u'Works outside Mochudi, home daily'),
    (u'works outside mochudi and comes home irregularly ', u'Works outside Mochudi, home irregularly '),
    (u'works outside mochudi and comes home monthly ', u'Works outside Mochudi, home monthly '),
    (u'works outside mochudi and comes home on weekends ', u'Works outside Mochudi, home on weekends '),
    (u'OTHER', u'Other...'),
)


RELATION = (
    ('spouse', 'spouse'),
    ('parent', 'parent'),
    ('sibling', 'sibling'),
    ('child', 'child'),
    ('aunt/uncle', 'aunt/uncle'),
    ('cousin', 'cousin'),
    ('partner', 'partner/boyfriend/girlfriend'),
    ('OTHER', 'Other, specify'),
)
