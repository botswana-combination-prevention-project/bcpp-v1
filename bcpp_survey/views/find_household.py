from django.shortcuts import render_to_response
from django.template import RequestContext
from bcpp_survey.forms import FindHouseholdForm
from bcpp_household.models import HouseholdStructure, HouseholdStructureMember 


def find_household(request, **kwargs):

    if request.method == 'POST':
        form = FindHouseholdForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # get a list of names, get rid of blanks and spaces
            first_names = [s for s in (cleaned_data['first_names'].replace(' ', '')).split(';') if s]
            # convert the list of names to a list of household_structure pks
            first_name_pks = []
            for name in first_names:
                household_structure_member = HouseholdStructureMember.objects.filter(first_name__icontains=name)
                if HouseholdStructureMember.objects.filter(first_name__icontains=name):
                    for hsm in HouseholdStructureMember.objects.filter(first_name__icontains=name): 
                        first_name_pks.append(hsm.household_structure.pk)
            first_name_pks = list(set(first_name_pks))
            queryset = HouseholdStructure.objects.filter(pk__in=first_name_pks).order_by('-created')
    else:
        queryset = None
    return queryset
