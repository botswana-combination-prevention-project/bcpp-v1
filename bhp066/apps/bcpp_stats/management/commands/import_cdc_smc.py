import csv

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand, CommandError

from ...models import CdcSmc


class Command(BaseCommand):

    args = '<source_path> <community_name>'
    help = 'Import CDC SMC data from csv'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        usage = 'Usage: import_cdc_smc <source_path> <community_name>'
        try:
            source_path = args[0]  # '/Users/erikvw/import_from_cdc/smc_23jul2014._otse_dsmb.csv'
        except IndexError:
            raise CommandError(usage)
        try:
            community = args[1].lower()
        except IndexError:
            raise CommandError(usage)
        header_row = []
#         row_list = []
#
#         title = ''
#         filename = source_path
#         description = ''
#         import_datetime = datetime.today()
        print 'importing file ' + source_path
        with open(source_path, 'r') as f:
            values = {}
            rows = csv.reader(f, delimiter=',')
            for i, row in enumerate(rows):
                # is_complete_row = True
                values = {}
                if not header_row:
                    header_row = row
                    for field in CdcSmc._meta.fields:
                        vl = [
                            'id', 'created', 'modified', 'user_created', 'user_modified',
                            'hostname_created', 'hostname_modified']
                        if field.name not in vl and field.name not in header_row:
                            header_row.append(field.name)
                else:
                    dob = None
                    reference_date = None
                    # do we have a subject identifier allocated by BHP, HTC or other
                    subject_identifier = row[header_row.index('mcVstSID')]
                    if not subject_identifier:
                        print 'Row {0}. Missing subject identifier'.format(i)
                    # dates are in odd formats, try to convert or fail
                    for field in CdcSmc._meta.fields:
                        lst = ['created', 'modified', '_import_datetime']
                        if 'Date' in field.get_internal_type() and field.name not in lst:
                            try:
                                dt = datetime.strptime(row[header_row.index(field.name)], '%d%b%y')
                                row[header_row.index(field.name)] = dt
                            except IndexError:
                                print field.name
                            except ValueError:
                                try:
                                    dt = datetime.strptime(row[header_row.index(field.name)][0:18], '%d%b%Y:%H:%M:%S')
                                    row[header_row.index(field.name)] = dt
                                except ValueError:
                                    print 'Row {0}. Unable to convert date string {1} to DateTime. Got {2}'.format(
                                        i, field.name, row[header_row.index(field.name)] or None)
                                    row[header_row.index(field.name)] = None
                            if field.name == 'mcVstInfoSourceDate':
                                reference_date = row[header_row.index(field.name)]
                            if field.name == 'mcVstInfoDOB':
                                dob = row[header_row.index(field.name)]
                    # OMANG may be of incorrect length or format or None
                    # we only assume 8 digits is just missing the leading 0
                    row_val = row[header_row.index('mcVstIDtypeOM')][4] in ['1', '2']
                    row_val1 = row[header_row.index('mcVstIDtypeOM')][3] in ['1', '2']
                    if len(row[header_row.index('mcVstIDtypeOM')]) == 9 and row_val:
                        pass
                    elif len(row[header_row.index('mcVstIDtypeOM')]) == 8 and row_val1:
                        row[header_row.index('mcVstIDtypeOM')] = '0' + row[header_row.index('mcVstIDtypeOM')]
                    elif not row[header_row.index('mcVstIDtypeOM')] and row[header_row.index('mcVstIDtypePBC')]:
                        pass
                    elif not row[header_row.index('mcVstIDtypeOM')] and row[header_row.index('mcVstIDtypePBC')]:
                        pass
                    else:
                        print 'Row {0}. Invalid OMANG in field {1}. Got {2}'.format(
                            i, 'mcVstIDtypeOM', row[header_row.index('mcVstIDtypeOM')] or 'None')

                    cdc_age_in_years = row[header_row.index('mcVstInfoAge')]
                    # populate dictionary for model.create
                    values = dict(zip(header_row, row))
                    # values.update({'_is_complete': is_complete_row})
                    values.update({'_title': source_path.split('/')[-1:]})
                    values.update({'_filename': source_path})
                    values.update({'_community': community})
                    if dob and reference_date:
                        age_in_years = relativedelta(reference_date, dob).years
                        if age_in_years != int(cdc_age_in_years):
                            print 'Row {0}. Calculated age_in_years does not match mcVstInfoAge '
                            'by {1}! Got {2}<>{3}'.format(
                                i, age_in_years - int(cdc_age_in_years), age_in_years, cdc_age_in_years)
                        if age_in_years < 16:
                            print 'Row {0}. Age_in_years under 16! Got {1}'.format(i, age_in_years)
                        if age_in_years > 105:
                            print 'Row {0}. Age_in_years over 105! Got {1}'.format(i, age_in_years)
                        values.update({'_age_in_years': age_in_years})
                    CdcSmc.objects.create(**values)
