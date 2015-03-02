from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

from apps.bcpp_subject.utils import update_call_list
from apps.bcpp_survey.models import Survey


class Command(BaseCommand):

    args = 'source-survey-slug label'
    help = 'Add to the call list info from all subject consents from the specified survey.'

    def handle(self, *args, **options):
        CallList = get_model('bcpp_subject', 'CallList')
        count = CallList.objects.all().count()
        try:
            survey_slug = args[0]
            Survey.objects.get(survey_slug=survey_slug)
        except (IndexError, Survey.DoesNotExist):
            raise CommandError('Specify a valid survey_slug')
        try:
            label = args[1]
        except IndexError:
            raise CommandError('Specify a label')
        update_call_list(survey_slug, label, verbose=True)
        new_count = CallList.objects.all().count()
        print 'Added {} records to the Call List for {}: {}.'.format(new_count - count, survey_slug, label)
