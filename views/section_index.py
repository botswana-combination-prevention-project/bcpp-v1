import re
from datetime import datetime, date
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from bhp_crypto.fields import BaseEncryptedField
from bhp_registration.models import RegisteredSubject
from bcpp_survey.models import Survey
from bcpp_survey.forms import FindHouseholdForm, FindHouseholdStructureMemberForm
from bcpp_household.models import HouseholdStructureMember, Household


@login_required
def section_index(request, **kwargs):

    """
    Renders a template for the given section name.

    Keyword Arguments:
      section_name:
      action:
      model_name:

    if action and model_name are known, display a lookup form
    if lookup form is submitted, do a lookup and return a paginated search_result queryset
    """
    section_name = kwargs.get('section_name')
    title = [section_name]
    template = 'section_%s.html' % (section_name)
    action = kwargs.get('action')
    by_model_name = kwargs.get('model_name', 'household')
    search_results = None
    surveys = Survey.objects.all().order_by('survey_name')
    selected_survey_slug, survey, allow_new = get_user_selected_survey(kwargs.get('survey'))
    if survey:
        title.append(survey.survey_name)
    if action == 'find':
        find_form, queryset = get_form_and_queryset(request, by_model_name)
    else:
        find_form = None
        queryset = get_default_queryset(section_name, selected_survey_slug)
    if queryset:
        paginator = Paginator(queryset, 15)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            search_results = paginator.page(page)
        except (EmptyPage, InvalidPage):
            search_results = paginator.page(paginator.num_pages)
    return render_to_response(template, {
        'surveys': surveys,
        'allow_new': allow_new,
        'selected': section_name,
        'selected_survey': survey,
        'include_template': '%s_include.html' % (by_model_name,),
        'form': find_form,
        'section_name': section_name,
        'search_results': search_results,
        'action': action,
        'model_name': by_model_name,
        'title': '{0}'.format('-'.join(title))
    }, context_instance=RequestContext(request))


def get_user_selected_survey(survey=None):
    allow_new = False
    # you might get "survey" as a pk, slug, or None
    if re.match('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', survey or ''):
        selected_survey_slug = Survey.objects.get(pk=survey).survey_slug
    else:
        selected_survey_slug = survey
    if selected_survey_slug:
        survey = Survey.objects.get(survey_slug=selected_survey_slug)
        if hasattr(settings, 'ALLOW_CHANGES_OTHER_SUVERYS') and settings.ALLOW_CHANGES_OTHER_SUVERYS:
            allow_new = True
        else:
            if survey:
                if survey.datetime_start <= datetime.today() and datetime.today() <= survey.datetime_end:
                    allow_new = True
    return selected_survey_slug, survey, allow_new


def get_form_and_queryset(request, by_model_name):
    """ Returns a tuple of (form, queryset) by selecting therequested form and if possible, validating its data to get a queryset of search results."""
    find_form = None
    queryset = None
    if by_model_name == 'household':
        find_form = FindHouseholdForm()
    if by_model_name == 'householdstructuremember':
        find_form = FindHouseholdStructureMemberForm()
    if request.method == 'POST':
        if by_model_name == 'household':
            find_form = FindHouseholdForm(request.POST)
        if by_model_name == 'householdstructuremember':
            find_form = FindHouseholdStructureMemberForm(request.POST)
        if find_form.is_valid():
            cleaned_data = find_form.cleaned_data
            if by_model_name == 'household':
                queryset = get_queryset(cleaned_data, Household)
            if by_model_name == 'householdstructuremember':
                queryset = get_queryset(cleaned_data, HouseholdStructureMember)
    return find_form, queryset


def get_default_queryset(section_name, survey_slug):
    queryset = None
    if survey_slug:
        if section_name == "household":
            count = Household.objects.all().aggregate(Count('household_identifier'))
            if count['household_identifier__count'] >= 15:
                queryset = Household.objects.all().order_by('-created', '-modified')[0:15]
            else:
                queryset = Household.objects.all().order_by('-created', '-modified')
        elif section_name == "mobile":
            if HouseholdStructureMember.objects.all().count() >= 15:
                queryset = HouseholdStructureMember.objects.all().order_by('-created', '-modified')[0:15]
            else:
                queryset = HouseholdStructureMember.objects.all().order_by('-created', '-modified')
    return queryset


def get_queryset(cleaned_data, model_cls, order_by=None):
    """Returns a queryset filtered on the criteria in cleaned data.

    The field to filter on may be an encrypted field and it may need to be accessed from
    :class:`RegisteredSubject` instead of the model class. If from an encrypted field
    check to see if the value can be encrypted and decrypted successfully (as a test
    for available keys). If not, hash the value to compare it to the stored hash.
    """

    if not order_by:
        order_by = '-created'
    options = {}
    # only consider these fields from registered subject
    registered_subject_fields = ['subject_identifier', 'dob', 'identity']
    encrypted_fields = {}
    # add encrypted field objects from registered subject
    for field in RegisteredSubject._meta.fields:
        if field.name in registered_subject_fields:
            if isinstance(field, BaseEncryptedField):
                encrypted_fields.update({field.name: field})
    # add encrypted field objects from this model class
    for field in model_cls._meta.fields:
        if isinstance(field, BaseEncryptedField):
            encrypted_fields.update({field.name: field})
    for fld, val in cleaned_data.iteritems():
        if val:
            if fld in encrypted_fields.keys():
                if val != encrypted_fields[fld].decrypt(encrypted_fields[fld].encrypt(val)):
                    #cannot be decrypted, so convert value to a hash
                    val = encrypted_fields[fld].field_cryptor.get_hash_with_prefix(val)
            if fld in registered_subject_fields:
                # modify the fld string to point to registered subject
                fld = 'registered_subject__{0}'.format(fld)
            if isinstance(val, (int, float)):
                options.update({'{0}'.format(fld): val})
            elif isinstance(val, (datetime, date)):
                options.update({'{0}'.format(fld): val})
            else:
                if val.lower() == 'none':
                    options.update({'{0}__isnull'.format(fld): True})
                elif val.lower() == 'all':
                    options.update({'{0}__isnull'.format(fld): False})
                elif re.search(r'\;', val):
                    lst = [v for v in (val.replace(' ', '')).split(';') if v]
                    options.update({'{0}__in'.format(fld): lst})
                else:
                    options.update({'{0}__icontains'.format(fld): val.replace(' ', '')})
    return model_cls.objects.filter(**options).order_by(order_by)
