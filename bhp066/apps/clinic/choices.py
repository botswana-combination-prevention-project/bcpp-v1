from django.utils.translation import ugettext as _


COMMUNITIES = (
        ('Bokaa', _('Bokaa')),
        ('Digawana', _('Digawana')),
        ('Gumare', _('Gumare')),
        ('Gweta', _('Gweta')),
        ('Lentsweletau', _('Lentsweletau')),
        ('Lerala', _('Lerala')),
        ('Letlhakeng', _('Letlhakeng')),
        ('Mandunyane', _('Mandunyane')),
        ('Mankgodi', _('Mankgodi')),
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
        ('Raikops', _('Raikops')),
        ('Ramokgonami', _('Ramokgonami')),
        ('Ranaka', _('Ranaka')),
        ('Sebina', _('Sebina')),
        ('Sefare', _('Sefare')),
        ('Sefophe', _('Sefophe')),
        ('Shakawe', _('Shakawe')),
        ('Shoshong', _('Shoshong')),
        ('Tati Siding', _('Tati Siding')),
        ('Tsetsebjwe', _('Tsetsebjwe')),
        ('OTHER', _('Other non study community')),
    )


VERBALHIVRESULT_CHOICE = (
        ('POS', _('HIV Positive')),
        ('NEG', _('HIV Negative')),
        ('UNK', _('I am not sure')),
        ('not_answering', _('Don\'t want to answer')),
    )

INABILITY_TO_PARTICIPATE_REASON = (
           ('Mental Incapacity', _('Mental Incapacity')),
           ('Deaf/Mute', _('Deaf/Mute')),
           ('Too sick to talk', _('Too sick to talk')),
           ('None', _('None')),
        )

YES_NO_DWTA = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('DWTA', _('Don\'t want to answer')),
)

OTHER_IDENTIFIERS = (
    ('barcode', 'Barcode Number'),
    ('Htc identifier', 'Htc identifier'),
    ('Pims identifier', 'Pims identifier'),
    ('Htc_Pims', 'Htc and Pims identifier'),
    ('Barcode_Pims', 'Barcode and Pims identifier'),
    ('None', 'None'),
    )

VISIT_UNSCHEDULED_REASON = (
    ('Routine oncology', _('Routine oncology clinic visit (i.e. planned chemo, follow-up)')),
    ('Ill oncology', _('Ill oncology clinic visit')),
    ('Patient called', _('Patient called to come for visit')),
    ('OTHER', _('Other, specify:')),
)

VISIT_REASON = (
    ('Initiation Visit', _('Initiation Visit')),
    ('MASA Scheduled VL Visit', _('MASA Scheduled Viral Load Visit')),
    ('CCC visit', _('CCC Enrolment Visit')),
    ('Other NON-VL Visit', _('Other NON-Viral Load Visit'))
    )

GENDER_UNDETERMINED = (
    ('M', 'Male'),
    ('F', 'Female'),
)
