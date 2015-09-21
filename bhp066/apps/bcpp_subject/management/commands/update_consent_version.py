from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from edc_consent.models import ConsentType
from ...models import SubjectConsent


class Command(BaseCommand):
    """ Corrects the version field in the subject consent"""
    args = '--fix <True|False>'

    help = ('Corrects the version field of the subject consent by re-saving the consent.'
            'Specify --fix (True|False) to fix or do a dry run')

    option_list = BaseCommand.option_list + (
        make_option(
            '--fix',
            dest='fix',
            action='store_true',
            default=False,
            help=('Fix or dry run')),
    )

    def handle(self, *args, **options):
        if len(args) == 1:
            pass
        else:
            raise CommandError('Command expecting a single argument being, --fix <True|False>')
        if options['fix']:
            self.resave_consents(args[0])
        else:
            raise CommandError('Command expecting a single argument being, --fix <True|False>')

    def resave_consents(self, fix):
        consents = SubjectConsent.objects.all()
        count = 0
        print "======================================="
        print "GOT {} CONSENTS".format(consents.count())
        for consent in consents:
            count += 1
            consent_type = ConsentType.objects.get_by_consent_datetime(
                consent.__class__, consent.consent_datetime
            )
            print ".....{}/{}, {}, will become version {}".format(count, consents.count(), consent, consent_type.version)
            if not fix:
                print ".....dry run, not saving {}".format(consent)
            else:
                consent.save(update_fields=['version'])
                print ".....persisted {}".format(consent)
