# import csv
# import os
# import pyodbc
#
# from dateutil.parser import parse
# from collections import namedtuple
#
# from django.conf import settings
#
# from bhp066.config.celery import app
#
#
# ReceivedTuple = namedtuple(
#     'ReceivedTuple',
#     'edc_specimen_identifier, lis_specimen_identifier, lis_patient_ref, received_datetime')
# ResultTuple = namedtuple(
#     'ResultTuple',
#     'edc_specimen_identifier, lis_specimen_identifier, lis_patient_ref, received_datetime, report_date, panel_id,
#       sample_assay_date, utestid, result, result_quantifier lis_result_id')
#
#
# class Dmis(object):
#     """Usage:
#
#         dmis = Dmis('/Users/erikvw/Documents/bcpp/rbd_subject_identifiers_20141202.csv',
#                     data_column_number=0,
#                     dmis_column='pat_id')
#         # load the source file of identifiers from the specifies column (data_column_numbers)
#         dmis.load()
#         # process, query the LIS and dump data back to a csv file.
#         dmis.dump()"""
#
#     def __init__(self, filename, data_column_numbers=[0], header=True,
#                  specimen_identifier_prefix=None, dmis_column=None, protocol_number=None,
#                  verbose=False):
#         self.identifiers = []
#         self.header_row = None
#         self.sql = {}
#         self.verbose = verbose
#         self.results = dict(received_items={},
#                             received_items_by_specimen_identifier={},
#                             resulted_items=[])
#         self.filename = filename
#         self.export_filename = (filename + '.resulted.csv') or '~/{}.resulted.csv'.format(protocol_number)
#         self.header = header
#         self.data_column_numbers = data_column_numbers
#         self.specimen_identifier_prefix = specimen_identifier_prefix
#         self.dmis_column = dmis_column or 'edc_specimen_identifier'
#         self.protocol_number = protocol_number
#
#     @app.task
#     def load_and_dump(self):
#         self.load()
#         self.dump()
#
#     def load(self):
#         """Loads the identifiers, queries for received and resulted items. Run dump() next."""
#         if self.protocol_number:
#             self.load_identifiers_from_dmis()
#         else:
#             self.load_identifiers_from_csv()
#         self.received_items
#         self.prepare_resulted_items()
#         self.resulted_items
#
#     def load_identifiers_from_dmis(self, protocol_number=None):
#         """Loads the list of identifiers from the dmis."""
#         def fetchall():
#             self.sql.update(
#                 dmis_identifiers=(
#                     'select {dmis_column} from lab01response as l where '
#                     'sample_protocolnumber=\'{protocol_number}\' order by {dmis_column}').format(
#                         dmis_column=self.dmis_column, protocol_number=self.protocol_number)
#                 )
#             return self.cursor.execute(self.sql.get('dmis_identifiers')).fetchall()
#         if self.verbose:
#             print "Loading identifiers from dmis for protocol number {}".format(self.protocol_number)
#             start_count = len(self.identifiers)
#         protocol_number = protocol_number or self.protocol_number
#         try:
#             with pyodbc.connect(settings.LAB_IMPORT_DMIS_DATA_SOURCE) as cnxn:
#                 with cnxn.cursor() as self.cursor:
#                     for row in fetchall():
#                         self.identifiers.append(row[0])
#         except pyodbc.Error:
#             raise
#         if self.verbose:
#             print "Loaded {} identifiers from dmis".format(len(self.identifiers) - start_count)
#         if self.filename:
#             self.load_identifiers_from_csv()
#         if self.verbose:
#             print "De-duplicating identifier list of {} identifiers".format(len(self.identifiers))
#         self.identifiers = list(set(self.identifiers))
#         if self.verbose:
#             print "Done. Load {} unique identifiers".format(len(self.identifiers))
#
#     def load_identifiers_from_csv(self):
#         """Loads a csv file of identifiers from the specified column number. (data_column_numbers)"""
#         if self.verbose:
#             print "Loading identifiers from csv file {}".format(self.filename)
#             start_count = len(self.identifiers)
#         self.header_row = None
#         with open(os.path.expanduser(self.filename)) as file_object:
#             rows = csv.reader(file_object)
#             for row in rows:
#                 if not self.header_row:
#                     self.header_row = row
#                 else:
#                     for column in self.data_column_numbers:
#                         if row[column]:
#                             self.identifiers.append(row[column])
#         if self.verbose:
#             print "Loaded {} identifiers from csv".format(len(self.identifiers) - start_count)
#         if self.verbose:
#             print "De-duplicating identifier list of {} identifiers from csv".format(
#                        len(self.identifiers) - start_count)
#         self.identifiers = list(set(self.identifiers))
#         if self.verbose:
#             print "Now have {} unique identifiers".format(len(self.identifiers))
#
#     def prepare_resulted_items(self):
#         """Prepares the resulted_items dictionary using \'lis_specimen_identifier\'
#         as the key from the data in the received_items dictionary."""
#         self.results['resulted_items'] = {}
#         for received_tuple in self.results.get('received_items').itervalues():
#             try:
#                 self.results.get('received_items_by_specimen_identifier')[received_tuple.lis_specimen_identifier] = \
#                     ResultTuple(
#                         received_tuple.edc_specimen_identifier,
#                         received_tuple.lis_specimen_identifier,
#                         received_tuple.lis_patient_ref,
#                         received_tuple.received_datetime,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None)
#             except AttributeError:
#                 pass
#
#     @property
#     def received_items(self):
#         """Fetches the receiving data from the LIS for each identifier."""
#         def fetchall():
#             self.sql.update(
#                 received_items=(
#        'select {dmis_column}, edc_specimen_identifier, pid, pat_id, headerdate from lab01response as l where '
#                     '{dmis_column} in (\'{search_list}\') order by {dmis_column}, headerdate').format(
#                         dmis_column=self.dmis_column, search_list='\',\''.join(self.identifiers))
#                 )
#             return self.cursor.execute(self.sql.get('received_items')).fetchall()
#         if self.verbose:
#             print "Querying dmis for {} received items".format(len(self.identifiers))
#         try:
#             with pyodbc.connect(settings.LAB_IMPORT_DMIS_DATA_SOURCE) as cnxn:
#                 with cnxn.cursor() as self.cursor:
#                     for
# selected_column, edc_specimen_identifier, lis_specimen_identifier, lis_patient_ref, received_datetime in fetchall():
#                         self.results.get('received_items').update(
#                             {selected_column:
#                              ReceivedTuple(
#                                  edc_specimen_identifier,
#                                  lis_specimen_identifier,
#                                  lis_patient_ref,
#                                  received_datetime)
#                              }
#                         )
#         except pyodbc.Error:
#             raise
#         for identifier in self.results.get('received_items'):
#             if identifier not in self.identifiers:
#                 self.results.get('received_items').update({identifier: []})
#         return self.results.get('received_items')
#
#     @property
#     def resulted_items(self):
#         """Fetches the result data for each received item in the received item dictionary.
#
#         May be more than one result per received item."""
#         def fetchall():
#             self.sql.update(
#                 resulted_items=(
# 'select PID as sample_id, reportdate, panel_id, sample_assay_date,
# utestid, result, result_quantifier, L21.id as lis_result_id '
#                     'from BHPLAB.DBO.LAB21Response as L21 '
#                     'left join BHPLAB.DBO.LAB21ResponseQ001X0 as L21D on L21.Q001X0=L21D.QID1X0 '
#                     'where PID in (\'{search_list}\') '
#                     'order by PID, reportdate').format(
#                         dmis_column=self.dmis_column, search_list='\',\''.join(
#  self.results.get('received_items_by_specimen_identifier').keys()))
#                 )
#             return self.cursor.execute(self.sql.get('resulted_items')).fetchall()
#         if self.verbose:
#             print "Querying dmis for {} resulted items".format(len(self.results.get(
# 'received_items_by_specimen_identifier').keys()))
#         try:
#             with pyodbc.connect(settings.LAB_IMPORT_DMIS_DATA_SOURCE) as cnxn:
#                 with cnxn.cursor() as self.cursor:
#                     for lis_specimen_identifier, report_date, panel_id, sample_assay_date, utestid, result,
# result_quantifier, lis_result_id in fetchall():
#                         received_tuple = self.results.get(
# 'received_items_by_specimen_identifier').get(lis_specimen_identifier)
#                         try:
#                             report_date = parse(report_date, dayfirst=True)
#                         except AttributeError:
#                             pass
#                         try:
#                             sample_assay_date = parse(sample_assay_date, dayfirst=True)
#                         except AttributeError:
#                             pass
#                         result_tuple = ResultTuple(
#                             received_tuple.edc_specimen_identifier,
#                             lis_specimen_identifier,
#                             received_tuple.lis_patient_ref,
#                             received_tuple.received_datetime,
#                             report_date,
#                             panel_id,
#                             sample_assay_date,
#                             utestid,
#                             result,
#                             result_quantifier,
#                             lis_result_id)
#                         try:
#                             self.results.get('resulted_items')[lis_specimen_identifier].append(result_tuple)
#                         except KeyError:
#                             self.results.get('resulted_items').update({lis_specimen_identifier: [result_tuple]})
#
#         except pyodbc.Error:
#             raise
#         return self.results.get('resulted_items')
#
#     def dump(self):
#         """Dump loaded result data to a csv file using the original
#         filename + 'resulted.csv' -- Run load() first."""
#         with open(os.path.expanduser(self.export_filename), 'w') as file_object:
#             writer = csv.writer(file_object)
#             writer.writerow(ResultTuple._fields)
#             for lis_specimen_identifier in self.results.get('received_items_by_specimen_identifier').keys():
#                 try:
#                     results = self.results.get('resulted_items')[lis_specimen_identifier]
#                 except KeyError:
#                     results = [self.results.get('received_items_by_specimen_identifier')[lis_specimen_identifier]]
#                 for result in results:
#                     writer.writerow([r for r in result])
