from django.utils.translation import ugettext as _

from edc.constants import NOT_APPLICABLE

YES_NO_DONT_ANSWER = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('not_answering', _('Don\'t want to answer')),
)

YES_NO_DWTA = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('DWTA', _('Don\'t want to answer')),
)

YES_NO_UNSURE_DWTA = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('not_sure', _('Not Sure')),
    ('not_answering', _('Don\'t want to answer')),
)

YES_NO_UNSURE = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('Not Sure', _('Not Sure')),
)

YES_NO_DONT_KNOW = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('Dont_know', _('Do not Know')),
)

YES_NO = (
    ('Yes', _('Yes')),
    ('No', _('No')),
)

YES_NO_REFUSED = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('Refuse', _('Refused to answer')),
)

# for some reason translations not reading this yes no though translation is available.


AGREE_STRONGLY = (
    ('Strongly disagree', _('Strongly disagree')),
    ('Disagree', _('Disagree')),
    ('Uncertain', _('Uncertain')),
    ('Agree', _('Agree')),
    ('Strongly agree', _('Strongly agree')),
    ('not_answering', _('Don\'t want to answer')),
)

SEXDAYS_CHOICE = (
    ('Days', _('Days')),
    ('Months', _('Months')),
    ('not_answering', _('Don\'t want to answer')),
)


LASTSEX_CHOICE = (
    ('Days', _('Days')),
    ('Months', _('Months')),
    ('Years', _('Years')),
    ('not_answering', _('Don\'t want to answer')),
)

LENGTHRESIDENCE_CHOICE = (
    ('Less than 6 months', _('Less than 6 months')),
    ('6 months to 12 months', _('6 months to 12 months')),
    ('1 to 5 years', _('1 to 5 years')),
    ('More than 5 years', _('More than 5 years')),
    ('not_answering', _('Don\'t want to answer')),
)

NIGHTSAWAY_CHOICE = (
    ('zero', _('Zero nights')),
    ('1-6 nights', _('1-6 nights')),
    ('1-2 weeks', _('1-2 weeks')),
    ('3 weeks to less than 1 month', _('3 weeks to less than 1 month')),
    ('1-3 months', _('1-3 months')),
    ('4-6 months', _('4-6 months')),
    ('more than 6 months', _('more than 6 months')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

FREQ_IN_YEAR = (
    ('Less than once a month', _('Less than once a month')),
    ('About once a month', _('About once a month')),
    ('2-3 times a month', _('2-3 times a month')),
    ('About once a week', _('About once a week')),
    ('2 or more times a week', _('2 or more times a week'))
)

CATTLEPOSTLANDS_CHOICE = (
    (NOT_APPLICABLE, _('Not Applicable')),
    ('Farm/lands', _('Farm/lands')),
    ('Cattle post', _('Cattle post')),
    ('Other community', _('Other community, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)

PARTIAL_PARTICIPATION_TYPE = (
        ('Not Applicable', _('Not Applicable')),
#         ('RBD Only', _('RBD Only')),
#         ('HTC Only', _('HTC Only')),
#         ('Questionnaires', _('Questionnaires only')),
        ('Changed mind midway', _('Participant changed mind')),
   )

COMMUNITIES = (
    ('Bokaa', _('Bokaa')),
    ('Digawana', _('Digawana')),
    ('Gumare', _('Gumare')),
    ('Gweta', _('Gweta')),
    ('Lentsweletau', _('Lentsweletau')),
    ('Lerala', _('Lerala')),
    ('Letlhakeng', _('Letlhakeng')),
    ('Mmandunyane', _('Mmandunyane')),
    ('Mmankgodi', _('Mmankgodi')),
    ('Mmadinare', _('Mmadinare')),
    ('Mmathethe', _('Mmathethe')),
    ('Masunga', _('Masunga')),
    ('Maunatlala', _('Maunatlala')),
    ('Mathangwane', _('Mathangwane')),
    ('Metsimotlhabe', _('Metsimotlhabe')),
    ('Molapowabojang', _('Molapowabojang')),
    ('Nata', _('Nata')),
    ('Nkange', _('Nkange')),
    ('Oodi', _('Oodi')),
    ('Otse', _('Otse')),
    ('Rakops', _('Rakops')),
    ('Ramokgonami', _('Ramokgonami')),
    ('Ranaka', _('Ranaka')),
    ('Sebina', _('Sebina')),
    ('Sefare', _('Sefare')),
    ('Sefophe', _('Sefophe')),
    ('Shakawe', _('Shakawe')),
    ('Shoshong', _('Shoshong')),
    ('Tati_Siding', _('Tati_Siding')),
    ('Tsetsebjwe', _('Tsetsebjwe')),
    ('OTHER', _('Other non study community')),
)

COMMUNITY_NA = (
    (NOT_APPLICABLE, _('Not Applicable')),
    ('Bokaa', _('Bokaa')),
    ('Digawana', _('Digawana')),
    ('Gumare', _('Gumare')),
    ('Gweta', _('Gweta')),
    ('Lentsweletau', _('Lentsweletau')),
    ('Lerala', _('Lerala')),
    ('Letlhakeng', _('Letlhakeng')),
    ('Mmandunyane', _('Mmandunyane')),
    ('Mmankgodi', _('Mmankgodi')),
    ('Mmadinare', _('Mmadinare')),
    ('Mmathethe', _('Mmathethe')),
    ('Masunga', _('Masunga')),
    ('Maunatlala', _('Maunatlala')),
    ('Mathangwane', _('Mathangwane')),
    ('Metsimotlhabe', _('Metsimotlhabe')),
    ('Molapowabojang', _('Molapowabojang')),
    ('Nata', _('Nata')),
    ('Nkange', _('Nkange')),
    ('Oodi', _('Oodi')),
    ('Otse', _('Otse')),
    ('Rakops', _('Rakops')),
    ('Ramokgonami', _('Ramokgonami')),
    ('Ranaka', _('Ranaka')),
    ('Sebina', _('Sebina')),
    ('Sefare', _('Sefare')),
    ('Sefophe', _('Sefophe')),
    ('Shakawe', _('Shakawe')),
    ('Shoshong', _('Shoshong')),
    ('Tati_Siding', _('Tati_Siding')),
    ('Tsetsebjwe', _('Tsetsebjwe')),
    ('OTHER', _('Other non study community')),
)
#     (NOT_APPLICABLE, _('Not Applicable')),
#     ('Cattle post or farm/lands', _('Cattle post or farm/lands')),
#     ('Work', _('Work')),
#     ('Education', _('Education')),
#     ('family/social events (wedding, funerals, holidays)', _('family/social events (wedding, funerals, holidays)')),
#     ('Other', _('Other')),
#     ('not_answering', _('Don\'t want to answer')),
# )


COMMUNITYENGAGEMENT_CHOICE = (
    ('Very active', _('Very active')),
    ('Somewhat active', _('Somewhat active')),
    ('Not active at all', _('Not active at all')),
    ('not_answering', _('Don\'t want to answer')),
)


VOTEENGAGEMENT_CHOICE = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('Not applicable', _('Not applicable (no election, can\'t vote)')),
    ('not_answering', _('Don\'t want to answer')),
)


SOLVEENGAGEMENT_CHOICE = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('dont_know', _('Don\'t know')),
    ('not_answering', _('Don\'t want to answer')),
)

RELIGION_CHOICE = (
    ('Anglican', _('Anglican')),
    ('Apostolic', _('Apostolic')),
    ('Baptist', _('Baptist')),
    ('Catholic', _('Catholic')),
    ('Methodist', _('Methodist')),
    ('Pentecostal', _('Pentecostal')),
    ('St John', _('St John')),
    ('ZCC', _('ZCC')),
    ('traditionalist', _('Traditionalist')),
    ('Hindu', _('Hinduism')),
    ('Islam', _('Islam')),
    ('Other', _('Other')),
    ('not_answering', _('Don\'t want to answer')),
)

ETHNIC_CHOICE = (
    ('Babirwa', _('Babirwa')),
    ('Bahambukushu', _('Bahambukushu')),
    ('Baherero', _('Baherero')),
    ('Bahurutshe', _('Bahurutshe')),
    ('Bakalaka', _('Bakalaka')),
    ('Bakgatla', _('Bakgatla')),
    ('Bakwena', _('Bakwena')),
    ('Balete', _('Balete')),
    ('Bangwaketse', _('Bangwaketse')),
    ('Bangwato', _('Bangwato')),
    ('Bakgalagadi', _('Bakgalagadi')),
    ('Basarwa', _('Basarwa')),
    ('Basobea', _('Basobea')),
    ('Batawana', _('Batawana')),
    ('Batlokwa', _('Batlokwa')),
    ('Batswapong', _('Batswapong')),
    ('White African', _('White African')),
    ('Indian African', _('Indian African')),
    ('Asian', _('Asian')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)

MARITALSTATUS_CHOICE = (
    ('Single/never married', _('Single/never married')),
    ('Married', _('Married (common law/civil or customary/traditional)')),
    ('Divorced/separated', _('Divorced or formally separated')),
    ('Widowed', _('Widowed')),
    ('not_answering', _('Don\'t want to answer')),
)


EDUCATION_CHOICE = (
    ('Non formal', _('Non formal')),
    ('Primary', _('Primary')),
    ('Junior Secondary', _('Junior Secondary')),
    ('Senior Secondary', _('Senior Secondary')),
    ('Higher than senior secondary (university, diploma, etc.)', _('Higher than senior secondary (university, diploma, etc.)')),
    ('not_answering', _('Don\'t want to answer')),
)

INABILITY_TO_PARTICIPATE_REASON = (
    (NOT_APPLICABLE, _('ABLE to participate')),
    ('Mental Incapacity', _('Mental Incapacity')),
    ('Deaf/Mute', _('Deaf/Mute')),
    ('Too sick', _('Too sick')),
    ('Incarcerated', _('Incarcerated')),
    ('OTHER', _('Other, specify.')),
)

EMPLOYMENT_CHOICE = (
    ('Not working', _('Not working')),
    ('Full-time Govt', _('Yes in the Government Sector (full time)')),
    ('Full-time Private', _('Yes in the Private Sector (full time)')),
    ('self employed-own', _('Yes self-employed working on my own')),
    ('self employed-employees', _('Yes self-employed working with employees')),
    ('part-time', _('Yes part-time/ intermittently')),
    ('Informal self-employment', _('Informal self-employment')),
    ('Student', _('Student')),
    ('Pensioner', _('Pensioner (retired)')),
    ('not_answering', _('Don\'t want to answer')),
)

HIV_RESULT = (
    ('POS', 'HIV Positive (Reactive)'),
    ('NEG', 'HIV Negative (Non-reactive)'),
    ('IND', 'Indeterminate'),
    ('Declined', 'Participant declined testing'),
    ('Not performed', 'Test could not be performed (e.g. supply outage, technical problem)'),
)

ELISA_HIV_RESULT = (
    ('POS', 'HIV Positive (Reactive)'),
    ('NEG', 'HIV Negative (Non-reactive)'),
)

WHYNOHIVTESTING_CHOICE = (
    ('I already knew I am HIV positive', _('I already knew I am HIV positive')),
    ('I recently tested', _('I recently tested (I know my status)')),
    ('I didn\'t believe I was at risk of getting HIV', _('I didn\'t believe I was at risk of getting HIV')),
    ('I am afraid to find out the result', _('I am afraid to find out the result')),
    ('I am afraid of what others would think of me', _('I am afraid of what others would think of me')),
    ('Family/friends did not want me to get an HIV test', _('Family/friends did not want me to get an HIV test')),
    ('I didn\'t have time due to work', _('I didn\'t have time due to work')),
    ('I didn\'t have time due to family obligations', _('I didn\'t have time due to family obligations')),
    ('My sexual partner did not want me to get an HIV test', _('My sexual partner did not want me to get an HIV test')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

RECORDEDHIVRESULT_CHOICE = (
    ('POS', 'HIV Positive (Reactive)'),
    ('NEG', 'HIV Negative (Non-reactive)'),
    ('IND', 'Indeterminate'),
    ('UNK', 'No result recorded'),
)

WHENHIVTEST_CHOICE = (
    ('In the last month', _('In the last month')),
    ('1 to 5 months ago', _('1 to 5 months ago')),
    ('6 to 12 months ago', _('6 to 12 months ago')),
    ('more than 12 months ago', _('more than 12 months ago')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

VERBALHIVRESULT_CHOICE = (
    ('POS', _('HIV Positive')),
    ('NEG', _('HIV Negative')),
    ('IND', _('Indeterminate')),
    ('UNK', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

WHEREHIVTEST_CHOICE = (
    ('Tebelopele VCT center', _('Tebelopele VCT center')),
    ('Antenatal care at healthcare facility', _('Antenatal care at healthcare facility (including private clinics)')),
    ('Other (not antenatal care) at healthcare facility', _('Other (not antenatal care) at healthcare facility (including private clinics)')),
    ('In my house as part of door-to-door services', _('In my house as part of door-to-door services')),
    ('In a mobile tent or vehicle in my neighborhood', _('In a mobile tent or vehicle in my neighborhood')),
    ('OTHER', _('Other, specify:')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

WHYHIVTEST_CHOICE = (
    ('I was worried I might have HIV and wanted to know my status', _('I was worried I might have HIV and wanted to know my status')),
    ('I heard from someone I trust that it is important for me to get tested for HIV ', _('I heard from someone I trust that it is important for me to get tested for HIV ')),
    ('I was at a health facility where the doctor/nurse recommended I get tested for HIV during the same visit', _('I was at a health facility where the doctor/nurse recommended I get tested for HIV during the same visit')),
    ('I read information on a brochure/flier that it is important for me to get tested for HIV', _('I read information on a brochure/flier that it is important for me to get tested for HIV')),
    ('Other', _('Other')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

HIVTEST_PREFEREDTIME = (
    ('Yes, specify', _('Yes, specify:')),
    ('No, any time of day is fine', _('No, any time of day is fine')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

HIVTEST_PREFEREDWEEK = (
    ('Yes, specify', _('Yes, specify:')),
    ('No, any day of the week is fine', _('No, any day of the week is fine')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)
HIVTEST_PREFEREDYEAR = (
    ('Yes, specify', _('Yes, specify:')),
    ('No, any month is fine', _('No, any month is fine')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

HIVTESTPREFERENCE_CHOICE = (
    ('At my home', _('At my home')),
    ('At a mobile testing tent or vehicle in my neighborhood', _('At a mobile testing tent or vehicle in my neighborhood')),
    ('At a health facility in my community', _('At a health facility in my community')),
    ('At a health facility or mobile testing unit outside of my community', _('At a health facility or mobile testing unit outside of my community')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

CIRCUMCISION_DAY = (
    ('Yes, specify:', _('Yes, specify:')),
    ('No, any time of day is fine', _('No, any time of day is fine')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

CIRCUMCISION_WEEK = (
    ('Yes, specify:', _('Yes, specify:')),
    ('No, any day of the week is fine', _('No, any day of the week is fine')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

CIRCUMCISION_MONTH = (
    ('Yes, specify:', _('Yes, specify:')),
    ('No, any month is fine', _('No, any month is fine')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

ALCOHOL_SEX = (
    ('Neither of us', _('Neither of us')),
    ('My partner', _('My partner')),
    ('Myself', _('Myself')),
    ('Both of us', _('Both of us')),
    ('not_answering', _('Don\'t want to answer')),
)

LASTSEX_CHOICE = (
    ('Days', _('Days')),
    ('Months', _('Months')),
    ('Years', _('Years')),
    ('not_answering', _('Don\'t want to answer')),
)

TIME_UNIT_CHOICE = (
        ('Days', _('Days')),
        ('Months', _('Months')),
        ('Years', _('Years')),
        ('not_answering', _('Don\'t want to answer')),
)

FIRSTPARTNERLIVE_CHOICE = (
    ('In this community', _('In this community')),
    ('On farm/cattle post', _('On farm/cattle post that is part of this community')),
    ('Outside this community', _('Outside this community')),
    ('Both in this community and outside this community', _('Both in this community and outside this community')),
    ('not_answering', _('Don\'t want to answer')),
)


FIRSTRELATIONSHIP_CHOICE = (
    ('Long-term partner', _('Long-term partner (>2 years) or spouse')),
    # ('2 years or spouse', _('2 years or spouse')),
    ('Boyfriend/Girlfriend', _('Boyfriend/Girlfriend')),
    ('Casual (known) partner', _('Casual (known) partner')),
    ('One time partner (previously unknown)', _('One time partner (previously unknown)')),
    ('Commercial sex worker', _('Commercial sex worker')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)


FIRSTPARTNERHIV_CHOICE = (
    ('positive', _('HIV-positive')),
    ('negative', _('HIV-negative')),
    ('not_sure', _('I am not sure HIV status')),
    ('not_answering', _('Don\'t want to answer')),
)


FIRSTDISCLOSE_CHOICE = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('Did not know my HIV status', _('Did not know my HIV status')),
    ('not_answering', _('Don\'t want to answer')),
)

AGE_RANGES = (
    (('less or equal to 18 years old'), _('less or equal to 18 years old')),
    (('19-29'), _('19-29 years old')),
    (('30-39'), _('30-39 years old')),
    (('40-49'), _('40-49 years old')),
    (('50-59'), _('50-59 years old')),
    (('50-59'), _('50-59 years old')),
    (('60 or older'), _('60 year or older')),
    (('Not sure'), _('Not sure'))
)

FIRSTCONDOMFREQ_CHOICE = (
    ('All of the time', _('All of the time')),
    ('Sometimes', _('Sometimes')),
    ('Never', _('Never')),
    ('not_answering', _('Don\'t want to answer')),
)

SECONDPARTNERLIVE_CHOICE = (
    ('In this community', _('In this community')),
    ('On farm/cattle post that is part of this community', _('On farm/cattle post that is part of this community')),
    ('Outside this community', _('Outside this community')),
    ('Both in this community and outside this community', _('Both in this community and outside this community')),
    ('not_answering', _('Don\'t want to answer')),
)

SECONDRELATIONSHIP_CHOICE = (
    ('2 years) or spouse', _('2 years) or spouse')),
    ('Boyfriend/Girlfriend', _('Boyfriend/Girlfriend')),
    ('Casual (known) partner', _('Casual (known) partner')),
    ('One time partner (previously unknown)', _('One time partner (previously unknown)')),
    ('Commercial sex worker', _('Commercial sex worker')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)


SECONDPARTNERHIV_CHOICE = (
    ('HIV-positive', _('HIV-positive')),
    ('HIV-negative', _('HIV-negative')),
    ('I am not sure HIV status', _('I am not sure HIV status')),
    ('not_answering', _('Don\'t want to answer')),
)


SECONDDISCLOSE_CHOICE = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('Did not know my HIV status', _('Did not know my HIV status')),
    ('not_answering', _('Don\'t want to answer')),
)

SECONDCONDOMFREQ_CHOICE = (
    ('All of the time', _('All of the time')),
    ('Sometimes', _('Sometimes')),
    ('Never', _('Never')),
    ('not_answering', _('Don\'t want to answer')),
)

THIRDPARTNERLIVE_CHOICE = (
    ('In this community', _('In this community')),
    ('On farm/cattle post that is part of this community', _('On farm/cattle post that is part of this community')),
    ('Outside this community', _('Outside this community')),
    ('Both in this community and outside this community', _('Both in this community and outside this community')),
    ('not_answering', _('Don\'t want to answer')),
)


THIRDRELATIONSHIP_CHOICE = (
    ('2 years) or spouse', _('2 years) or spouse')),
    ('Boyfriend/Girlfriend', _('Boyfriend/Girlfriend')),
    ('Casual (known) partner', _('Casual (known) partner')),
    ('One time partner (previously unknown)', _('One time partner (previously unknown)')),
    ('Commercial sex worker', _('Commercial sex worker')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)

THIRDPARTNERHIV_CHOICE = (
    ('HIV-positive', _('HIV-positive')),
    ('HIV-negative', _('HIV-negative')),
    ('I am not sure HIV status', _('I am not sure HIV status')),
    ('not_answering', _('Don\'t want to answer')),
)

THIRDDISCLOSE_CHOICE = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('I did not know my HIV status', _('I did not know my HIV status')),
    ('not_answering', _('Don\'t want to answer')),
)

THIRDCONDOMFREQ_CHOICE = (
    ('All of the time', _('All of the time')),
    ('Sometimes', _('Sometimes')),
    ('Never', _('Never')),
    ('not_answering', _('Don\'t want to answer')),
)

LOWESTCD4_CHOICE = (
    ('0-49', _('0-49')),
    ('50-99', _('50-99')),
    ('100-199', _('100-199')),
    ('200-349', _('200-349')),
    ('350-499', _('350-499')),
    ('500 or more', _('500 or more')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

NO_MEDICAL_CARE = (
    ('Did not feel sick', _('Did not feel sick')),
    ('Did not know I should get HIV care', _('Did not know I should get HIV care')),
    ('Did not have time due to work responsibilities', _('Did not have time due to work responsibilities')),
    ('Did not have time due to family/childcare responsibilities', _('Did not have time due to family/childcare responsibilities')),
    ('Transportation costs', _('Transportation costs')),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic', _('Was afraid of someone (friends/family) seeing me at the HIV clinic')),
    ('Traditional healer advised against going', _('Traditional healer advised against going')),
    ('Religious beliefs', _('Religious beliefs')),
    ('Cultural beliefs', _('Cultural beliefs')),
    ('OTHER', _('Other, specify:')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

WHYNOARV_CHOICE = (
    ('Did not feel sick', _('Did not feel sick')),
    ('Was afraid treatment would make me feel bad/sick', _('Was afraid treatment  would make me feel bad/sick')),
    ('Difficulty finding someone to go with me for counseling (mopati)', _('Difficulty finding someone to go with me for counseling (mopati)')),
    ('Hard due to work responsibilities', _('Hard due to work responsibilities')),
    ('Hard due to family/childcare responsibilities', _('Hard due to family/childcare responsibilities')),
    ('Transportation costs', _('Transportation costs')),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic', _('Was afraid of someone (friends/family) seeing me at the HIV clinic')),
    ('Sexual partner advised against taking', _('Sexual partner advised against taking')),
    ('Family or friends advised against taking', _('Family or friends advised against taking')),
    ('Traditional healer advised against taking', _('Traditional healer advised against taking')),
    ('Religious beliefs', _('Religious beliefs')),
    ('Cultural beliefs', _('Cultural beliefs')),
    ('High CD4', _('High CD4')),
    ('Other', _('Other, specify:')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

WHYARVSTOP_CHOICE = (
    ('Did not feel they were helping', _('Did not feel they were helping')),
    ('ARVs made me feel bad or sick', _('ARVs made me feel bad or sick')),
    ('Difficulty finding someone to go with me for counseling (mopati)', _('Difficulty finding someone to go with me for counseling (mopati)')),
    ('Hard due to work responsibilities', _('Hard due to work responsibilities')),
    ('Hard due to family/childcare responsibilities', _('Hard due to family/childcare responsibilities')),
    ('Doctor or nurse at clinic told me to stop', _('Doctor or nurse at clinic told me to stop')),
    ('Transportation costs', _('Transportation costs')),
    ('Was afraid of someone (friends/family) seeing me at the HIV clinic', _('Was afraid of someone (friends/family) seeing me at the HIV clinic')),
    ('Sexual partner advised against taking', _('Sexual partner advised against taking')),
    ('Family or friends advised against taking', _('Family or friends advised against taking')),
    ('Traditional healer advised against taking', _('Traditional healer advised against taking')),
    ('Religious beliefs', _('Religious beliefs')),
    ('Cultural beliefs', _('Cultural beliefs')),
    ('Other', _('Other, specify:')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

ADHERENCE4DAY_CHOICE = (
    ('Zero', _('Zero days')),
    ('One day', _('One day')),
    ('Two days', _('Two days')),
    ('Three days', _('Three days')),
    ('Four days', _('Four days')),
    ('not_answering', _('Don\'t want to answer')),
)

ADHERENCE4WK_CHOICE = (
    ('Very poor', _('Very poor')),
    ('Poor', _('Poor')),
    ('Fair', _('Fair')),
    ('Good', _('Good')),
    ('Very good', _('Very good')),
    ('not_answering', _('Don\'t want to answer')),
)


REASONCIRC_CHOICE = (
    ('Circumcision never offered to me', _('Circumcision never offered to me')),
    ('Procedure might be painful', _('Procedure might be painful')),
    ('Did not know where to go for circumcision', _('Did not know where to go for circumcision')),
    ('Did not have the time or money for circumcision', _('Did not have the time or money for circumcision')),
    ('I might not be able to work or be active', _('I might not be able to work or be active')),
    ('My partner might not approve', _('My partner might not approve')),
    ('My family/friends might not approve', _('My family/friends might not approve')),
    ('There might be a medical complication', _('There might be a medical complication')),
    ('The healing time is very long', _('The healing time is very long')),
    ('It will be hard to not have sex or masturbate for 6 weeks', _('It will be hard to not have sex or masturbate for 6 weeks')),
    ('Sex might not feel the same', _('Sex might not feel the same')),
    ('I may not like the way my penis looks', _('I may not like the way my penis looks')),
    ('I may not like the way my penis feels', _('I may not like the way my penis feels')),
    ('I could die from the procedure', _('I could die from the procedure')),
    ('OTHER', _('Other, specify:')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

WHYNOHIVTEST_CHOICE = (
    ('Yes, specify:', _('Yes, specify:')),
    ('No, any month is fine', _('No, any month is fine')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

FUTUREREASONSSMC_CHOICE = (
    ('More information about benefits', _('More information about benefits')),
    ('More information about risks', _('More information about risks')),
    ('If there was no or minimal pain with circumcision', _('If there was no or minimal pain with circumcision')),
    ('If circumcision could be done close to my home', _('If circumcision could be done close to my home')),
    ('If the kgosi recommended circumcision for all men', _('If the kgosi recommended circumcision for all men')),
    ('If I received time off work to recover from circumcision', _('If I received time off work to recover from circumcision')),
    ('If my sexual partner encouraged me', _('If my sexual partner encouraged me')),
    ('If one or both of my parents encouraged me', _('If one or both of my parents encouraged me')),
    ('If my friends encouraged me', _('If my friends encouraged me')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

AWAREFREE_CHOICE = (
    ('Radio', _('Radio')),
    ('Television', _('Television')),
    ('Friend told me', _('Friend told me')),
    ('Family told me', _('Family told me')),
    ('Health worker told me', _('Health worker told me')),
    ('Kgosi told us', _('Kgosi told us')),
    ('I heard it at the kgotla', _('I heard it at the kgotla')),
    ('I read a brochure delivered to my home', _('I read a brochure delivered to my home')),
    ('I read it in the newspaper', _('I read it in the newspaper')),
    ('Heard it at a community event', _('Heard it at a community event')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

PLACE_CIRC = (
    ('Government clinic or hospital', _('Government clinic or hospital')),
    ('Traditional location (Bogerwa)', _('Traditional location (Bogerwa)')),
    ('Outreach site (mobile or temporary center)', _('Outreach site (mobile or temporary center)')),
    ('Private practitioner', _('Private practitioner')),
    ('not_sure', _('I am not sure')),
    ('Other', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)

WHYCIRC_CHOICE = (
    ('Prevent HIV/AIDS', _('Prevent HIV/AIDS')),
    ('Other medical reason', _('Other medical reason')),
    ('Personal preference', _('Personal preference')),
    ('Improved hygiene', _('Improved hygiene')),
    ('Cultural tradition and/or religion', _('Cultural tradition and/or religion')),
    ('Acceptance by sexual partner(s)', _('Acceptance by sexual partner(s)')),
    ('Acceptance by family, friends, and/or community', _('Acceptance by family, friends, and/or community')),
    ('not_sure', _('I am not sure')),
    ('Other', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)

WHERECIRC_CHOICE = (
    ('Yes', _('Yes')),
    ('No, not sexually active and will not become sexual active', _('No, not sexually active and will not become sexual active')),
    ('No, prior surgical sterilization', _('No, prior surgical sterilization')),
    ('No, partner(s) surgically sterilized', _('No, partner(s) surgically sterilized')),
    ('No, post-menopause', _('No, post-menopause (at least 24 consecutive months without a period)')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)


ANCREG_CHOICE = (
    ('Yes', _('Yes')),
    ('No, but I will go for antenatal care', _('No, but I will go for antenatal care')),
    ('No and I am not planning on going for antenatal care', _('No and I am not planning on going for antenatal care')),
    ('not_answering', _('Don\'t want to answer')),
)


PREGARV_CHOICE = (
    ('Yes, AZT (single drug, twice a day)', _('Yes, AZT (single drug, twice a day)')),
    ('Yes, HAART ', _('Yes, HAART [multiple drugs like Atripla, Truvada, or Combivir taken once or twice a day]')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
    ('No', _('No ARV\'s')),
)


DXHEARTATTACK_CHOICE = (
    ('Myocardial infarction (heart attack)', _('Myocardial infarction (heart attack)')),
    ('Congestive cardiac failure', _('Congestive cardiac failure')),
    ('Stroke (cerebrovascular accident, CVA)', _('Stroke (cerebrovascular accident, CVA)')),
    ('Other', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)


DXCANCER_CHOICE = (
    ('Kaposi\'s sarcoma (KS)', 'Kaposi\'s sarcoma (KS)'),
    ('Cervical cancer', 'Cervical cancer'),
    ('Breast cancer', 'Breast cancer'),
    ('Non-Hodgkin\'s lymphoma (NHL)', 'Non-Hodgkin\'s lymphoma (NHL)'),
    ('Colorectal cancer', 'Colorectal cancer'),
    ('Prostate cancer', 'Prostate cancer'),
    ('Cancer of mouth, throat, voice box (larynx)', 'Cancer of mouth, throat, voice box (larynx)'),
    ('Cancer of oesophagus', 'Cancer of oesophagus'),
    ('Other', 'Other, specify:'),
    ('not_answering', 'Don\'t want to answer'),
)


DXTB_CHOICE = (
    ('Pulmonary tuberculosis', 'Pulmonary tuberculosis'),
    ('Extrapulmonary (outside the lungs) tuberculosis', 'Extrapulmonary (outside the lungs) tuberculosis'),
    ('Other', 'Other, specify:'),
    ('not_answering', 'Don\'t want to answer'),
)

ALCOHOL_CHOICE = (
    ('Never', _('Never')),
    ('Less then once a week', _('Less then once a week')),
    ('Once a week', _('Once a week')),
    ('2 to 3 times a week', _('2 to 3 times a week')),
    ('more than 3 times a week', _('more than 3 times a week')),
    ('not_answering', _('Don\'t want to answer')),
)

WHEREACCESS_CHOICE = (
    ('Traditional, faith, or religious healer/doctor', _('Traditional, faith, or religious healer/doctor')),
    ('Pharmacy', _('Pharmacy')),
    ('Public or government', _('Public or government health facility or clinic')),
    ('Private health facility', _('Private health facility or clinic')),
    ('Community health worker', _('Community health worker')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)

OVERALLACCESS_CHOICE = (
    ('Strongly disagree', _('Strongly disagree')),
    ('Disagree', _('Disagree')),
    ('Uncertain', _('Uncertain')),
    ('Agree', _('Agree')),
    ('Strongly agree', _('Strongly agree')),
    ('not_answering', _('Don\'t want to answer')),
)


MOBILTYQOL_CHOICE = (
    ('I have no problems in walking about', _('I have no problems in walking about')),
    ('I have slight problems in walking about', _('I have slight problems in walking about')),
    ('I have moderate problems in walking about', _('I have moderate problems in walking about')),
    ('I have severe problems in walking about', _('I have severe problems in walking about')),
    ('I am unable to walk about', _('I am unable to walk about')),
    ('not_answering', _('Don\'t want to answer')),
)

SELFCAREQOL_CHOICE = (
    ('I have no problems washing or dressing myself', _('I have no problems washing or dressing myself')),
    ('I have slight problems washing or dressing myself', _('I have slight problems washing or dressing myself')),
    ('I have moderate problems washing or dressing myself', _('I have moderate problems washing or dressing myself')),
    ('I have severe problems washing or dressing myself', _('I have severe problems washing or dressing myself')),
    ('I am unable to wash or dress myself', _('I am unable to wash or dress myself')),
    ('not_answering', _('Don\'t want to answer')),
)

ACTIVITIESQOL_CHOICE = (
    ('I have no problems doing my usual activities', _('I have no problems doing my usual activities')),
    ('I have slight problems doing my usual activities', _('I have slight problems doing my usual activities')),
    ('I have moderate problems doing my usual activities', _('I have moderate problems doing my usual activities')),
    ('I have severe problems doing my usual activities', _('I have severe problems doing my usual activities')),
    ('I am unable to do my usual activities', _('I am unable to do my usual activities')),
    ('not_answering', _('Don\'t want to answer')),
)
PAINQOL_CHOICE = (
    ('I have no pain or discomfort', _('I have no pain or discomfort')),
    ('I have slight pain or discomfort', _('I have slight pain or discomfort')),
    ('I have moderate pain or discomfort', _('I have moderate pain or discomfort')),
    ('I have severe pain or discomfort', _('I have severe pain or discomfort')),
    ('I have extreme pain or discomfort', _('I have extreme pain or discomfort')),
    ('not_answering', _('Don\'t want to answer')),
)
ANXIETYQOL_CHOICE = (
    ('I am not anxious or depressed', _('I am not anxious or depressed')),
    ('I am slightly anxious or depressed', _('I am slightly anxious or depressed')),
    ('I am moderately anxious or depressed', _('I am moderately anxious or depressed')),
    ('I am severely anxious or depressed', _('I am severely anxious or depressed')),
    ('I am extremely anxious or depressed', _('I am extremely anxious or depressed')),
    ('not_answering', _('Don\'t want to answer')),
)


RECENTVISIT_CHOICE = (
    ('Government Primary Health Clinic/Post', _('Government Primary Health Clinic/Post')),
    ('Chemist/Pharmacy', _('Chemist/Pharmacy')),
    ('Hospital Outpatient Department (including government and private)', _('Hospital Outpatient Department (including government and private)')),
    ('Private Doctor', _('Private Doctor')),
    ('Traditional or Faith Healer', _('Traditional or Faith Healer')),
    ('No visit in past 3 months', _('No visit in past 3 months')),
    ('not_answering', _('Don\'t want to answer')),
)

REVISIT3MO_CHOICE = (
    ('HIV-related care, including TB and other opportunistic infections', _('HIV-related care, including TB and other opportunistic infections')),
    ('Pregnancy-related care, including delivery', _('Pregnancy-related care, including delivery')),
    ('Injuries or accidents', _('Injuries or accidents')),
    ('Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness', _('Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness')),
    ('Other', _('Other')),
    ('not_answering', _('Don\'t want to answer')),
)

TIMETOCLINIC3MO_CHOICE = (
    ('Under 0.5 hour', _('Under 0.5 hour')),
    ('0.5 to under 1 hour', _('0.5 to under 1 hour')),
    ('1 to under 2 hours', _('1 to under 2 hours')),
    ('2 to under 3 hours', _('2 to under 3 hours')),
    ('More than 3 hours', _('More than 3 hours')),
    ('not_answering', _('Don\'t want to answer')),
)

WAITCOSTS_CHOICE = (
    ('Under 0.5 hour', _('Under 0.5 hour')),
    ('0.5 to under 1 hour', _('0.5 to under 1 hour')),
    ('1 to under 2 hours', _('1 to under 2 hours')),
    ('2 to under 3 hours', _('2 to under 3 hours')),
    ('3 or more hours', _('3 or more hours')),
    ('not_answering', _('Don\'t want to answer')),
)

REHOSPMO_CHOICE = (
    ('HIV-related care, including TB and other opportunistic infections', _('HIV-related care, including TB and other opportunistic infections')),
    ('Pregnancy-related care, including delivery', _('Pregnancy-related care, including delivery')),
    ('Injuries or accidents', _('Injuries or accidents')),
    ('Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness', _('Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness')),
    ('Other', _('Other')),
    ('not_answering', _('Don\'t want to answer')),
)

TIMETOHOSP3MO_CHOICE = (
    ('Under 0.5 hour', _('Under 0.5 hour')),
    ('0.5 to under 1 hour', _('0.5 to under 1 hour')),
    ('1 to under 2 hours', _('1 to under 2 hours')),
    ('2 to under 3 hours', _('2 to under 3 hours')),
    ('More than 3 hours', _('More than 3 hours')),
    ('not_answering', _('Don\'t want to answer')),
)

HIVNOCARECOSTS_CHOICE = (
    ('I am not thinking about HIV related medical/clinical care at this time', _('I am not thinking about HIV related medical/clinical care at this time')),
    ('HIV related medical/clinical care for my HIV infection is important to me but I am not ready to start it yet', _('HIV related medical/clinical care for my HIV infection is important to me but I am not ready to start it yet')),
    ('I have thought about starting HIV related medical/clinical care but have not yet tried to find a doctor or clinic', _('I have thought about starting HIV related medical/clinical care but have not yet tried to find a doctor or clinic')),
    ('I have found a doctor or clinic for HIV related medical/clinical care but have not yet tried to make an appointment', _('I have found a doctor or clinic for HIV related medical/clinical care but have not yet tried to make an appointment')),
    ('I have tried to obtain HIV related medical/clinical care from a doctor or clinic but have not been successful yet', _('I have tried to obtain HIV related medical/clinical care from a doctor or clinic but have not been successful yet')),
    ('I have an appointment for HIV related medical/clinical care for my HIV infection but have not been for it yet', _('I have an appointment for HIV related medical/clinical care for my HIV infection but have not been for it yet')),
    ('I don\'t know where to go for HIV related medical/clinical care', _('I don\'t know where to go for HIV related medical/clinical care')),
    ('I do not have the money for HIV related medical/clinical care', _('I do not have the money for HIV related medical/clinical care')),
    ('not_answering', _('Don\'t want to answer')),
)

HIVCARELOCATIONCOSTS_CHOICE = (
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
    ('not_answering', _('Don\'t want to answer')),
)

HIVCARETIMESCOSTS_CHOICE = (
    ('0 times', _('0 times')),
    ('1 time', _('1 time')),
    ('2 times', _('2 times')),
    ('3 times', _('3 times')),
    ('4 times', _('4 times')),
    ('5 times', _('5 times')),
    ('6-10 times', _('6-10 times')),
    ('More than 10 times', _('More than 10 times')),
    ('not_answering', _('Don\'t want to answer')),
)

HIVACCOMPANYCOSTS_CHOICE = (
    ('All of the time (always)', _('All of the time (always)')),
    ('Most of the time (almost always)', _('Most of the time (almost always)')),
    ('Some of the time (sometimes)', _('Some of the time (sometimes)')),
    ('Almost none of the time (rarely)', _('Almost none of the time (rarely)')),
    ('None of the time (never)', _('None of the time (never)')),
    ('not_answering', _('Don\'t want to answer')),
)

EMPLOYEDCOSTS_CHOICE = (
    ('Yes, In the government sector', _('Yes, In the government sector')),
    ('Yes, in the private sector', _('Yes, in the private sector')),
    ('Yes, self-employed working on my own', _('Yes, self-employed working on my own')),
    ('Yes, self-employed with own employees', _('Yes, self-employed with own employees')),
    ('No, not working', _('No, not working')),
    ('not_answering', _('Don\'t want to answer')),
)

OCCUPATIONCOSTS_CHOICE = (
    ('Farmer (own land)', _('Farmer (own land)')),
    ('Farm worker (work on employers land)', _('Farm worker (work on employers land)')),
    ('Domestic Worker', _('Domestic Worker')),
    ('Work at Tavern/Bar/Entertainment Venue', _('Work at Tavern/Bar/Entertainment Venue')),
    ('Mining', _('Mining')),
    ('Tourism/game parks', _('Tourism/game parks')),
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
    ('not_answering', _('Don\'t want to answer')),
)


WORKINCOMECOSTS_CHOICE = (
    ('1-200 pula', _('1-200 pula')),
    ('200-499 pula', _('200-499 pula')),
    ('500-999 pula', _('500-999 pula')),
    ('1000-4999 pula', _('1000-4999 pula')),
    ('5000-10,000 pula', _('5000-10,000 pula')),
    ('More than 10,000 pula', _('More than 10,000 pula')),
    ('not_answering', _('Don\'t want to answer')),
)

PLOT_LOG_STATUS = (
    ('ABSENT', 'Household(s) Absent'),
    ('PRESENT', 'Household(s) Present'),
    ('INACCESSIBLE', 'Inaccessible'),
)

WORKPAIDCOSTS_CHOICE = (
    ('Fixed salary', _('Fixed salary')),
    ('Paid daily', _('Paid daily')),
    ('Paid hourly', _('Paid hourly')),
    ('not_answering', _('Don\'t want to answer')),
)

HOUSEHOLDINCOMECOSTS_CHOICE = (
    ('1-200 pula', _('1-200 pula')),
    ('200-499 pula', _('200-499 pula')),
    ('500-999 pula', _('500-999 pula')),
    ('1000-4999 pula', _('1000-4999 pula')),
    ('5000-10,000 pula', _('5000-10,000 pula')),
    ('10,0000-20,000 pula', _('10,0000-20,000 pula')),
    ('More than 20,000 pula', _('More than 20,000 pula')),
    ('not_sure', _('I am not sure')),
    ('not_answering', _('Don\'t want to answer')),
)

NONWORKACTIVITIESCOSTS_CHOICE = (
    ('Studying', _('Studying')),
    ('Doing housework', _('Doing housework')),
    ('Looking for work', _('Looking for work')),
    ('Doing nothing (not looking for paid work)', _('Doing nothing (not looking for paid work)')),
    ('Retired/old age', _('Retired/old age')),
    ('Pregnant or recently pregnant', _('Pregnant or recently pregnant')),
    ('Sick or injured', _('Sick or injured')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)


WHYNOPARTICIPATE_CHOICE = (
    ('I don\'t have time', _('I don\'t have time')),
    ('I don\'t want to answer the questions', _('I don\'t want to answer the questions')),
    ('I don\'t want to have the blood drawn', _('I don\'t want to have the blood drawn')),
    ('I am afraid my information will not be private', _('I am afraid my information will not be private')),
    ('Fear of needles', _('Fear of needles')),
    ('Illiterate does not want a witness', _('Illiterate does not want a witness')),
    ('I already know I am HIV-positive', _('I already know I am HIV-positive')),
    ('I am afraid of testing', _('I am afraid of testing')),
    ('I don\'t want to take part', _('I don\'t want to take part')),
    ('I haven\'t had a chance to think about it', _('I haven\'t had a chance to think about it')),
    ('Have a newly born baby, not permitted', _('Have a newly born baby, not permitted')),
    ('I am not ready to test', _('I am not ready to test')),
    ('Already on HAART', _('Already on HAART')),
    ('I want to test where i always test', _('I want to test where i always test')),
    ('I already know my partner\'s status, no need to test', _('I already know my partner\'s status, no need to test')),
    ('The appointment was not honoured', _('The appointment was not honoured')),
    ('not_sure', _('I am not sure')),
    ('OTHER', _('Other, specify:')),
    ('not_answering', _('Don\'t want to answer')),
)

GENDER_UNDETERMINED = (
    ('M', 'Male'),
    ('F', 'Female'),
)

MEDICAL_CARE = (
    ('Doctor', _('Doctor')),
    ('Nurse', _('Nurse')),
    ('Traditional healer', _('Traditional healer')),
    ('Both clinician and traditional healer', _('Both clinician and traditional healer')),
    ('No known medical care received (family/friends only)', _('No known medical care received (family/friends only)')),
    ('Unknown', _('Unknown')),
)

RELATIONSHIP_STUDY = (
    ('Definitely not related', _('Definitely not related')),
    ('Probably not related', _('Probably not related')),
    ('Possible related', _('Possible related')),
    ('Probably related', _('Probably related')),
    ('Definitely related', _('Definitely related')),
)

EASY_OF_USE = (
    ('easy', _('Easy')),
    ('Very easy', _('Very Easy')),
    ('Fairly easy', _('Fairly easy')),
    ('Difficult', _('Difficult')),
    ('Very difficult', _('Very difficult')),
)

