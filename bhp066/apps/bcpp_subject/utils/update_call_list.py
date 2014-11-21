from django.db.models import get_model

from config.celery import app

from edc.constants import NEW
from apps.bcpp_survey.models import Survey
from apps.bcpp_household.models import HouseholdStructure
from apps.bcpp_household_member.models import HouseholdMember


@app.task
def update_call_list(survey_slug, label):
    """Adds information from SubjectConsent instances from the specified survey to the
    CallList model for the current survey.

    If needed, the household member for the next survey will be created.
    See (HouseholdStructure manager method add_household_members_from_survey).
    """
    SubjectReferral = get_model('bcpp_subject', 'SubjectReferral')
    CallList = get_model('bcpp_subject', 'CallList')
    HicEnrollment = get_model('bcpp_subject', 'HicEnrollment')
    SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
    SubjectLocator = get_model('bcpp_subject', 'SubjectLocator')
    consent_options = dict(household_member__household_structure__survey__survey_slug=survey_slug)
    options = {}
    for subject_consent in SubjectConsent.objects.filter(**consent_options).order_by('subject_identifier'):
        try:
            SubjectLocator.objects.get(
                subject_visit__household_member=subject_consent.household_member,
                may_follow_up='Yes')
            try:
                hic_enrollment = HicEnrollment.objects.get(
                    subject_visit__household_member=subject_consent.household_member,
                    hic_permission='Yes')
                options.update(
                    hic=True,
                    hic_datetime=hic_enrollment.report_datetime
                    )
            except HicEnrollment.DoesNotExist:
                options.update(
                    hic=False,
                    hic_datetime=None,
                    )
            try:
                subject_referral = SubjectReferral.objects.get(
                    subject_visit__household_member=subject_consent.household_member)
                options.update(
                    referral_code=subject_referral.referral_code,
                    referral_appt_date=subject_referral.referral_appt_date,
                    )
            except SubjectReferral.DoesNotExist:
                pass
            household = subject_consent.household_member.household_structure.household
            source_survey = subject_consent.household_member.household_structure.survey
            target_survey = Survey.objects.current_survey()
            HouseholdStructure.objects.add_household_members_from_survey(
                household, source_survey, target_survey)
            household_structure = HouseholdStructure.objects.get(
                household=household,
                survey=target_survey)
            target_household_member = HouseholdMember.objects.get(
                household_structure=household_structure,
                internal_identifier=subject_consent.household_member.internal_identifier)
            options.update(
                household_member=target_household_member,
                community=household.plot.community,
                first_name=target_household_member.first_name,
                initials=target_household_member.initials,
                age_in_years=target_household_member.age_in_years,
                gender=target_household_member.gender,
                subject_identifier=subject_consent.subject_identifier,
                app_label=SubjectConsent._meta.app_label,
                object_name=SubjectConsent._meta.object_name,
                object_pk=subject_consent.pk,
                bhs=True,
                consent_datetime=subject_consent.consent_datetime,
                call_status=NEW,
                label=label,
                )
            try:
                CallList.objects.get(household_member=target_household_member, label=label)
            except CallList.DoesNotExist:
                CallList.objects.create(**options)
        except SubjectLocator.DoesNotExist:
            pass
