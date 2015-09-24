from __future__ import print_function

import sys

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from bhp066.apps.bcpp_subject.models import SubjectConsent
from edc_consent.models.consent_type import ConsentType


class Command(BaseCommand):
    help = ('Updates the subject consent version field from \'?\'.')

    def handle(self, *args, **options):
        self.resave_consents()

    def resave_consents(self):
        consents = SubjectConsent.objects.filter(version='?')
        count = 0
        failed = 0
        total = consents.count()
        print("Updating {} consents where version == \'?\' ... ".format(total))
        sys.stdout.flush()
        for consent in consents:
            count += 1
            try:
                consent_type = ConsentType.objects.get_by_consent_datetime(
                    SubjectConsent, consent.consent_datetime)
                consent.version = consent_type.version
                consent.save_base(update_fields=['version'])
            except ValidationError:
                failed += 1
                print('              failed = {} \r'.format(failed), end="")
            print('{} / {} \r'.format(count, total), end="")
            sys.stdout.flush()
        print('{} failed on a ValidationErorr'.format(failed))
        print("Done.")
