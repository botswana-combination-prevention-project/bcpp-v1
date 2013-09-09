#from optparse import make_option
#import logging
#from django.core.management.base import BaseCommand, CommandError
#from lab_clinic_reference.classes import ImportGrading, ImportReferenceRange
#
#logger = logging.getLogger(__name__)
#
#
#class NullHandler(logging.Handler):
#    def emit(self, record):
#        pass
#nullhandler = logger.addHandler(NullHandler())
#
#
#class Command(BaseCommand):
#
#    args = (' --grading --reference-range --all')
#    help = 'Imports grading and / or reference range lists from the lis based on the list names in your settings.py. '
#    option_list = BaseCommand.option_list + (
#        make_option('--grading',
#            action='store_true',
#            dest='import_grading',
#            default=False,
#            help=('Import grading table from Lis (lap_api).')),
#         )
#    option_list += (
#        make_option('--reference-range',
#            action='store_true',
#            dest='import_reference_range',
#            default=False,
#            help=('Import reference range table from Lis (lap_api).')),
#        )
#    option_list += (
#        make_option('--all',
#            action='store_true',
#            dest='import_all',
#            default=False,
#            help=('Import both grading and reference range tables from Lis (lap_api).')),
#        )
#
#    def handle(self, *args, **options):
#        db = 'lab_api'
#        if options['import_grading']:
#            self.import_grading(db)
#        elif options['import_reference_range']:
#            self.import_reference_range(db)
#        elif options['import_all']:
#            self.import_grading(db)
#            self.import_reference_range(db)
#        else:
#            raise CommandError('Unknown option, Try --help for a list of valid options')
#
#    def import_grading(self, db):
#        import_grading = ImportGrading(db)
#        import_grading.import_list()
#
#    def import_reference_range(self, db):
#        import_reference_range = ImportReferenceRange(db)
#        import_reference_range.import_list()
