from django import forms
from django.forms.widgets import Select
from apps.bcpp_household_member.choices import HOUSEHOLD_MEMBER_ACTION


class ParticipationForm(forms.Form):
    """A form to select the type of participation for a household member.

    ...note:: configured and referenced directly on the household_member model via method participation_form()"""
#     def __init__(self, *args, **kwargs):
#         super(ParticipationForm, self).__init__()
#         HOUSEHOLD_MEMBER_HTC = [
#                         ('NOT_REPORTED', '<not reported>'),
#                         ('HTC', 'HTC'),
#                         ]
#         age = kwargs.get('age')
#         residency = kwargs.get('residency')
#         if age and age >= 64:
#             self.status = forms.ChoiceField(choices=HOUSEHOLD_MEMBER_HTC, widget=Select(attrs={'onchange': 'this.form.submit();'}))
#         if residency and residency == 'No':
#             self.status = forms.ChoiceField(choices=HOUSEHOLD_MEMBER_HTC, widget=Select(attrs={'onchange': 'this.form.submit();'}))

#     residency = forms.CharField(widget=forms.HiddenInput())
#     age = forms.IntegerField(widget=forms.HiddenInput())
    status = forms.ChoiceField(choices=HOUSEHOLD_MEMBER_ACTION, widget=Select(attrs={'onchange': 'this.form.submit();'}))
    household_member = forms.CharField(widget=forms.HiddenInput())
    dashboard_type = forms.CharField(widget=forms.HiddenInput())
    dashboard_id = forms.CharField(widget=forms.HiddenInput())
    dashboard_model = forms.CharField(widget=forms.HiddenInput())

    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row=u'<td>%(errors)s%(field)s%(help_text)s</td>',
            error_row=u'<tr><td colspan="2">%s</td></tr>',
            row_ender=u'</td>',
            help_text_html=u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)
