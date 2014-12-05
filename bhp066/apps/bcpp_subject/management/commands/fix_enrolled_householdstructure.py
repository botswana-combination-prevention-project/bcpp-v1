from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model
from django.core.exceptions import MultipleObjectsReturned, ValidationError

from edc.constants import YES

from apps.bcpp_household_member.constants import BHS, BHS_ELIGIBLE, BHS_SCREEN
from apps.bcpp_household.models.representative_eligibility import RepresentativeEligibility
from apps.bcpp_household_member.models.enrollment_checklist import EnrollmentChecklist


class Command(BaseCommand):

    args = ''
    help = 'Resave all consents to set household_structure enrolled and add Representative Eligibility'

    option_list = BaseCommand.option_list + (
        make_option('--representative-eligibility',
            action='store_true',
            dest='representative-eligibility',
            default=False,
            help=('Auto-create missing RepresentativeEligibility.')),
         )
    option_list += (
        make_option('--resave-consent',
            action='store_true',
            dest='resave-consents',
            default=False,
            help=('Resave consents.')),
        )

    def handle(self, *args, **options):
        SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')
        total = SubjectConsent.objects.all().count()

        if options['representative-eligibility']:
            self.create_representative_eligibility()
        elif options['resave-consents']:
            self.resave_consent()
        else:
            raise CommandError('Valid options are --representative_eligibility and --resave_consent.')

    def household_member(self, subject_consent):
        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')
        try:
            household_member = HouseholdMember.objects.get(
                relation='head',
                household_structure=subject_consent.household_member.household_structure)
        except HouseholdMember.DoesNotExist:
            household_member = subject_consent.household_member
        except MultipleObjectsReturned:
            household_member = HouseholdMember.objects.filter(
                relation='head',
                household_structure=subject_consent.household_member.household_structure)[0]
        return household_member

    def create_representative_eligibility(self):
        SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
        total = SubjectConsent.objects.all().count()
        n = 0
        print 'auto-creating RepresentativeEligibility'
        for subject_consent in SubjectConsent.objects.all().order_by('subject_identifier'):
            n += 1
            household_member = self.household_member(subject_consent)
            options = dict(
                household_structure=subject_consent.household_member.household_structure,
                auto_filled=True,
                report_datetime=household_member.created,
                aged_over_18=YES,
                household_residency=YES,
                verbal_script=YES)
            try:
                RepresentativeEligibility.objects.get(household_structure=subject_consent.household_member.household_structure)
            except RepresentativeEligibility.DoesNotExist:
                RepresentativeEligibility.objects.create(**options)
            print '{}/{} {}'.format(n, total, subject_consent.subject_identifier)

    def resave_consent(self):
        SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
        total = SubjectConsent.objects.all().count()
        n = 0
        print 're-saving updating consent and create enrollment checklist if required'
        for subject_consent in SubjectConsent.objects.all().order_by('subject_identifier'):
            n += 1
            if subject_consent.modified < datetime(2014, 11, 30):
                subject_consent.household_member.member_status = BHS_SCREEN
                subject_consent.household_member.household_structure.household.plot.status = 'residential_habitable'
                try:
                    EnrollmentChecklist.objects.get(household_member=subject_consent.household_member)
                except EnrollmentChecklist.DoesNotExist:
                    options = dict(
                        household_member=subject_consent.household_member,
                        report_datetime=subject_consent.created,
                        initials=subject_consent.initials,
                        dob=subject_consent.dob,
                        guardian=subject_consent.is_minor,
                        gender=subject_consent.gender,
                        has_identity=YES,
                        citizen=subject_consent.citizen,
                        legal_marriage=subject_consent.legal_marriage,
                        marriage_certificate=subject_consent.marriage_certificate,
                        part_time_resident=YES,
                        household_residency=YES,
                        literacy=YES,
                        is_eligible=True,
                        auto_filled=True)
                    EnrollmentChecklist.objects.create(**options)
                subject_consent.household_member.member_status = BHS
                # subject_consent.household_member.save()
                try:
                    subject_consent.save()
                except ValidationError as e:
                    print '{} {}'.format(subject_consent.subject_identifier, str(e))
                print '{}/{} {}'.format(n, total, subject_consent.subject_identifier)
