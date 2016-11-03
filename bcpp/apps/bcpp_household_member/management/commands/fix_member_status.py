from django.core.management.base import BaseCommand
from django.db.models import get_model
from bhp066.apps.bcpp_household_member.constants import ANNUAL, BHS
from bhp066.apps.bcpp_household.constants import BASELINE_SURVEY_SLUG


class Command(BaseCommand):

    args = 'run'
    help = 'Update member status for ANNUAL members who consented in the baseline survey'

    def handle(self, *args, **options):
        dry_run = True
        try:
            if args[0] == 'run':
                dry_run = False
        except IndexError:
            pass
        if dry_run:
            print 'dry-run'
        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')
        # if consented at baseline, set YEAR 2, etc member to ANNUAL
        member_count = HouseholdMember.objects.exclude(
            household_structure__survey__survey_slug=BASELINE_SURVEY_SLUG).count()
        print 'Found {} ANNUAL household members to update'.format(member_count)
        n = 0
        for household_member in HouseholdMember.objects.exclude(
                household_structure__survey__survey_slug=BASELINE_SURVEY_SLUG):
            try:
                if HouseholdMember.objects.get(
                        internal_identifier=household_member.internal_identifier,
                        household_structure__survey__survey_slug=BASELINE_SURVEY_SLUG).member_status == BHS:
                    household_member.member_status = ANNUAL
                    if not dry_run:
                        household_member.save_base(update_fields=['member_status'])
                    n += 1
                    print '    updated {} {}/{}'.format(household_member, n, member_count)
            except HouseholdMember.DoesNotExist:
                print 'Not enumerated in baseline survey. {}'.format(household_member)
        print 'Done'
