import os

from django.core.management.base import BaseCommand

from ...models import SubjectReferral


class Command(BaseCommand):

    args = ''
    help = 'resaves bcpp_subject.subject_referral and prints appt if changed.'

    def handle(self, *args, **options):
        for subject_referral in SubjectReferral.objects.all():
            referral_appt_date = subject_referral.referral_appt_date
            print subject_referral
            subject_referral.save()
            if referral_appt_date != subject_referral.referral_appt_date:
                print '  {} {}'.format(subject_referral.referral_appt_date, referral_appt_date)
