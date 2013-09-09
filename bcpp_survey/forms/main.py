from django import forms


class FindHouseholdForm(forms.Form):
    household_identifier = forms.CharField(
        max_length=15,
        label="Household Identifier",
        help_text="enter all or part of the household identifier",
        required=False,
        #error_messages={'required': 'Please enter a valid netbook hostname.'},
        )
    cso_number = forms.CharField(
        max_length=4,
        label="CSO",
        help_text="enter all or part of the CSO number",
        required=False,
        error_messages={'required': 'Please enter a host hostname.'},
        )
    ward = forms.CharField(
        label="Ward",
        help_text="enter all or part of the ward",
        required=False,
        #choices = MOCHUDI_WARDS,
        #initial = None,
        error_messages={'required': 'Please enter a host hostname.'},
        )
    gps = forms.CharField(
        max_length=15,
        label="GPS",
        help_text="enter GPS coordinates",
        required=False,
        error_messages={'required': 'Please enter a host hostname.'},
        )


class FindHouseholdStructureMemberForm(forms.Form):

    subject_identifier = forms.CharField(
        max_length=16,
        label="Subject Identifier",
        help_text="enter all or part of the subject identifier",
        required=False,
        #error_messages={'required': 'Please enter a valid netbook hostname.'},
        )
    first_name = forms.CharField(
        max_length=25,
        label="First name(s)",
        help_text="if more than one name, separate by \';\'",
        required=False,
        )
    initials = forms.CharField(
        max_length=3,
        label="Initials",
        required=False,
        )
    identity = forms.CharField(
        max_length=25,
        label="Identity",
        help_text="OMANG, passport, etc",
        required=False,
        )
    age_in_years = forms.IntegerField(
        label="Age",
        help_text="age in years",
        required=False,
        )
    dob = forms.DateField(
        label="Date of Birth",
        help_text="Format is DD/MM/YYYY",
        required=False,
        )
    gender = forms.CharField(
        label="Gender (M/F)",
        help_text="M/F",
        required=False,
        )
