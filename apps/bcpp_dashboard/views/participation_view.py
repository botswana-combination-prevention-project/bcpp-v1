from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

from apps.bcpp_household_member.forms import ParticipationForm
from apps.bcpp_household_member.models import HouseholdMember


class ParticipationView(FormView):
    # template_name =
    form_class = ParticipationForm
    success_url = 'household_dashboard_url'

    def form_valid(self, form):
        household_member = HouseholdMember.objects.get(id=form.cleaned_data.get('household_member'))
        if form.cleaned_data.get('status'):
            household_member.member_status = form.cleaned_data.get('status')
            household_member.save(update_fields=['member_status'])
            self.success_url = reverse(
                'household_dashboard_url',
                kwargs=dict(dashboard_type=form.cleaned_data.get('dashboard_type'),
                            dashboard_model=form.cleaned_data.get('dashboard_model'),
                            dashboard_id=form.cleaned_data.get('dashboard_id'),
                            )
                )
        return super(ParticipationView, self).form_valid(form)

#     def form_invalid(self, form):
#         """
#         If the form is invalid, re-render the context data with the
#         data-filled form and errors.
#         """
#         self.success_url = reverse(
#             'household_dashboard_url',
#             kwargs=dict(dashboard_type=form.cleaned_data.get('dashboard_type'),
#                         dashboard_model=form.cleaned_data.get('dashboard_model'),
#                         dashboard_id=form.cleaned_data.get('dashboard_id'),
#                         )
#             )
#         return super(ParticipationView, self).form_valid(form)
