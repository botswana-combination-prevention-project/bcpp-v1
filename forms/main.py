from django import forms
from django.forms.widgets import Select
from bcpp_household.choices import HOUSEHOLD_MEMBER_ACTION


class ParticipationForm(forms.Form):

    status = forms.ChoiceField(choices=HOUSEHOLD_MEMBER_ACTION, widget=Select(attrs={'onchange': 'this.form.submit();'}))
    household_structure_member = forms.CharField(widget=forms.HiddenInput())
    dashboard_type = forms.CharField(widget=forms.HiddenInput())
    survey = forms.CharField(widget=forms.HiddenInput())

    def as_table(self):
        "Returns this form rendered as HTML <tr>s -- excluding the <table></table>."
        return self._html_output(
            normal_row=u'<td>%(errors)s%(field)s%(help_text)s</td>',
            error_row=u'<tr><td colspan="2">%s</td></tr>',
            row_ender=u'</td>',
            help_text_html=u'<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)
