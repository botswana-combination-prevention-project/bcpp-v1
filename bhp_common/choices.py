from django.utils.translation import ugettext_lazy as _


# choices
BLANK_CHOICE_DASH = [('', '---------')]

""" Try to keep this in alphabetical order """

ACU_EST = (
    ('Acute', 'Acute'),
    ('Established', 'Established'),
)

ACU_EST_NEG = (
    ('Acute', 'Acute'),
    ('Established', 'Established'),
    ('Negative', 'Negative'),
)

ALIVE_DEAD = (
    ('alive', 'Alive'),
    ('dead', 'Dead'),
    )

ALIVE_DEAD_UNKNOWN = (
    ('alive', 'Alive'),
    ('dead', 'Dead'),
    ('unknown', 'Unknown'),
    )

ART_STATUS = (
    ('ON', 'Yes, ON ART'),
    ('STOPPED', 'No, stopped ART'),
    ('NAIVE', 'No, have never taken ART'),
)

ART_STATUS_UNKNOWN = (
    ('ON', 'ON ART'),
    ('STOPPED', 'Stopped'),
    ('NAIVE', 'Naive'),
    ('UNKNOWN', 'Unknown'),

)

ART_STATUS_CONFIRM = (
    ('OPD', '1. Show OPD/IDCC card'),
    ('Pills', '2. Show Pills'),
    ('Pic', '3. Identify Pictorial'),
)

CONFIRMED_SUSPECTED = (
    ('CONFIRMED', 'Confirmed'),
    ('SUSPECTED', 'Suspected'),
)

COUNTRY = (
    ('botswana', 'Botswana'),
    ('zimbabwe', 'Zimbabwe'),
    ('rsa', 'South Africa'),
    ('zambia', 'Zambia'),
    ('namibia', 'Namibia'),
    ('nigeria', 'Nigeria'),
    ('china', 'China'),
    ('india', 'India'),
    ('OTHER', 'Other'),
    )

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    ('AnyDay', 'Any Day'),
)

TIME_OF_DAY = (
    ('Morning', 'Morning'),
    ('Afternoon', 'Afternoon'),
    ('Evening', 'Evening'),
    ('Anytime', 'Anytime'),
)


DATE_ESTIMATED = (
    ('-', 'No'),
    ('D', 'Yes, estimated the Day'),
    ('MD', 'Yes, estimated Month and Day'),
    ('YMD', 'Yes, estimated Year, Month and Day'),
)


DRUG_FORMULATION = (
    ('11', 'Tablet'),
    ('12', 'Capsule'),
    ('13', 'Liquid'),
    ('14', 'Powder'),
    ('15', 'Suspension'),
    ('16', 'Gel'),
    ('17', 'Oil'),
    ('18', 'Lotion'),
    ('19', 'Cream'),
    ('20', 'Patch'),
    ('99', 'Other'),
)

DRUG_ROUTE = (
    ('1', 'Intramuscular'),
    ('2', 'Intravenous'),
    ('3', 'Oral'),
    ('4', 'Topical'),
    ('5', 'Subcutaneous'),
    ('6', 'Intravaginal'),
    ('7', 'Rectal'),
    ('9', 'Other'),
)

FEEDING = (
   ('BF', 'Breast Feed'),
   ('FF', 'Formula Feed'),
)

GENDER = (
    ('M', _('Male')),
    ('F', _('Female')),
)

GENDER_UNDETERMINED = (
    ('M', _('Male')),
    ('F', _('Female')),
    ('U', _('Undetermined')),
)

"""do not change without inspecting implication to check_omang_field() in utils.py"""
IDENTITY_TYPE = (
    ('OMANG', 'Omang'),
    ('DRIVERS', 'Driver\'s License'),
    ('PASSPORT', 'Passport'),
    ('OMANG_RCPT', 'Omang Receipt'),
    ('OTHER', 'Other'),
)


NORMAL_ABNORMAL = (
    ('NORMAL', 'Normal'),
    ('ABNORMAL', 'Abnormal'),
)

NORMAL_ABNORMAL_NOEXAM = (
    ('NORMAL', 'Normal'),
    ('ABNORMAL', 'Abnormal'),
    ('NO_EXAM', 'No Exam Performed'),
)

NORMAL_ABNORMAL_NOTEVALUATED = (
    ('NORMAL', 'Normal'),
    ('ABNORMAL', 'Abnormal'),
    ('NOT_EVAL', 'Not Evaluated'),
)

POS_NEG = (
    ('POS', 'Positive'),
    ('NEG', 'Negative'),
    ('IND', 'Indeterminate'),
)

POS_NEG_REFUSED = (
    ('POS', 'Positive'),
    ('NEG', 'Negative'),
    ('IND', 'Indeterminate'),
    ('REF', 'Refused to disclose'),
)

POS_NEG_ANY = (
    ('POS', 'Positive'),
    ('NEG', 'Negative'),
    ('ANY', 'Any'),
)

POS_NEG_ONLY = (
    ('POS', _('Positive')),
    ('NEG', _('Negative')),
)

POS_NEG_UNKNOWN = (
    ('POS', _('Positive')),
    ('NEG', _('Negative')),
    ('UNKNOWN', _('Unknown')),
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


POS_NEG_UNTESTED_REFUSAL = (
    ('POS', 'Positive'),
    ('NEG', 'Negative'),
    ('NEVER', 'Never tested for HIV'),
    ('UNK', 'Unknown'),
    ('REFUSED', 'Refused to answer'),
)

REFUSAL_STATUS = (
    ('REFUSED', 'Refused'),
    ('NOT_REFUSED', 'No longer refusing'),
)

SEVERITY_LEVEL = (
    ('mild', 'Mild'),
    ('moderate', 'Moderate'),
    ('severe', 'Severe'),
)

SEXUAL_DEBUT = (
    ('<=14', '14 or under'),
    ('15-17', ' 15 - 17'),
    ('>=18', '18 or above'),
)

TIME_UNITS = (
    ('TODAY', 'Today'),
    ('DAYS', 'Days'),
    ('WEEKS', 'Weeks'),
    ('MONTHS', 'Months'),
    ('YEARS', 'Years'),
)

URINALYSIS = (
    ('NAD', 'NAD'),
    ('Sugar Neg', 'Sugar Neg'),
    ('Sugar +', 'Sugar +'),
    ('Sugar ++', 'Sugar ++'),
    ('Sugar +++', 'Sugar +++'),
    ('Blood', 'Blood'),
    ('Protein', 'Protein'),
    ('Cells', 'Cells'),
    )

WILL_DECL = (
    ('WILLING', 'Willing'),
    ('DELINED', 'Declined'),
)

YES_NO = (
    ('Yes', _('Yes')),
    ('No', _('No')),
)

YES_NO_OPTIONAL = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Optional', 'Optional'),
)

YES_NO_REFUSED = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('REF', _('Refused to answer')),
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

YES_NO_NOT_EVALUATED = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not_evaluated', 'Not evaluated'),
)

YES_NO_NOT_EVALUATED_NA = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not_evaluated', 'Not evaluated'),
    ('N/A', 'Not applicable'),
)

YES_NO_NOT_DONE = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not_done', 'Not Done'),
)

YES_NO_DOESNT_WORK = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('DontWork', 'Doesn\'t work'),
)

YES_NO_UNKNOWN = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Unknown', 'Unknown'),
)

YES_NO_UNKNOWN_NA = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Unknown', 'Unknown'),
    ('N/A', 'Not applicable'),
)

YES_NO_UNSURE = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not Sure', 'Not Sure'),
)

YES_NO_UNSURE_NA = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not Sure', 'Not Sure'),
    ('N/A', 'Not Applicable'),
)

YES_NO_DONT_KNOW = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Dont_know', 'Do not Know'),
)

YES_NO_DONT_KNOW_NA = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Dont_know', 'Do not Know'),
    ('N/A', 'Not applicable'),
)

YES_NO_DOESNT_WORK = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Doesnt_work', 'Doesnt Work'),
)
