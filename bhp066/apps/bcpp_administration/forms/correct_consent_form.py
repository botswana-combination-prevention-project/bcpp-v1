from django import forms


class CorrectConsentForm(forms.Form):
    subject_identifier = forms.CharField(label='Subject identifier', required=True)
    lastname = forms.CharField(label='Lastname', required=False)
    firstname = forms.CharField(label='Firstname', required=False,)
    initials = forms.CharField(label='Initials', required=False)
    guardian_name = forms.CharField(label='Gaurdian name', required=False)
    is_literate = forms.CharField(label='Is literate', required=False)
    dob = forms.DateField(label='dob', required=False)
    gender = forms.CharField(label='Gender', required=False)
    may_store_samples = forms.CharField(label='Sample storage', required=False)

    def clean_subject_identifier(self):
        subject_identifier = self.cleaned_data['subject_identifier']
        if subject_identifier is None:
            raise forms.ValidationError("subject_identifier is required")
        return subject_identifier
