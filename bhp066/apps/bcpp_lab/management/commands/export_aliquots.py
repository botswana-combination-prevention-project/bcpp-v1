import csv

from django.core.management.base import BaseCommand, CommandError

from ...models import Aliquot


class Command(BaseCommand):

    args = ''
    help = 'Export aliquots.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):

        with open('/tmp/aliquot.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['requisition_identifier', 'drawn_datetime', 'aliquot_identifier', 'aliquot_type', 'aliquot_datetime', 'subject_identifier', 'initials', 'dob', 'requisition_model_name', 'receive_identifier'])
            for a in Aliquot.objects.all():
                writer.writerow([a.receive.requisition_identifier,
                                 a.receive.drawn_datetime,
                                 a.aliquot_identifier,
                                 a.aliquot_type, a.aliquot_datetime,
                                 a.receive.registered_subject.subject_identifier,
                                 a.receive.registered_subject.initials,
                                 a.receive.registered_subject.dob,
                                 a.receive.requisition_model_name,
                                 a.receive.receive_identifier])
