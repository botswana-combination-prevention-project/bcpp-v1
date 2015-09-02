from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

from apps.bcpp_household_member.constants import ANNUAL
from apps.bcpp_household.constants import BASELINE_SURVEY_SLUG


class Command(BaseCommand):

    args = 'survey_slug'
    help = ('Update member updated_after_auto_filled AT THE START of the annual survey '
            '(ONLY and after running fix member_status correcting BHS to ANNUAL)')

    def handle(self, *args, **options):
        error_log = open('fix_updated_after_auto_filled.txt', 'w')
        survey_slug = '?'
        try:
            survey_slug = args[0] or '?'
            if survey_slug == BASELINE_SURVEY_SLUG:
                raise CommandError('Parameter survey_slug cannot be {}'.format(survey_slug))
        except IndexError:
            CommandError('Please specify a survey_slug')
        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')
        # if consented at baseline, set YEAR 2, etc member to ANNUAL
        household_members = HouseholdMember.objects.filter(
            household_structure__survey__survey_slug=survey_slug)
        member_count = household_members.count()
        print 'Found {} ANNUAL household members from survey {} to update'.format(member_count, survey_slug)
        total_saved, n, m = 0, 0, 0
        print 'Updating ...'
        for household_member in household_members:
            household_member.updated_after_auto_filled = True if household_member.member_status == ANNUAL else False
            if household_member.updated_after_auto_filled:
                m += 1
            else:
                n += 1
            try:
                household_member.save_base(update_fields=['updated_after_auto_filled'])
                total_saved += 1
                print("{}/{} Saved household member: {}".format(total_saved, member_count, household_member))
            except Exception as e:
                error_log.write("Error on: Member: {} {}\n".format(household_member, e))
                print("Failed for household member: {}".format(household_member))
        print ('Done updating updated_after_auto_filled to False in {} rows and '
               'True in {} for survey {}.').format(n, m, survey_slug)
