from __future__ import print_function

import pyodbc

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Count

from edc.map.classes import site_mappers

from ..models import PackingListItem, Aliquot


class PackingListHelper(object):

    def __init__(self):
        self.cursor = None

    @property
    def received_items(self):
        community_code = site_mappers.get_mapper(site_mappers.current_community).map_code
        sql = ('select headerdate, edc_specimen_identifier from lab01response as l where '
               'edc_specimen_identifier like \'066{}%\'').format(community_code)
        return self.cursor.execute(sql).fetchall()

    @property
    def stored_items(self):
        community_code = site_mappers.get_mapper(site_mappers.current_community).map_code
        sql = ('select datecreated, sample_id, sample_type from ST505ResponseQ001X0 where '
               'sample_id like \'066{}%\'').format(community_code)
        return self.cursor.execute(sql).fetchall()

    def update_packing_list_item(self, packing_list_item, received_datetime):
        packing_list_item.received_datetime = received_datetime
        packing_list_item.received = True
        packing_list_item.save(update_fields=['received', 'received_datetime'])

    def reconcile_with_destination(self, exception_cls=None, print_messages=None):
        """Flags packing list items as received based on queries into LIS database at
        settings.LAB_IMPORT_DMIS_DATA_SOURCE.

        Queries BHHRL LIS receiving records and storage records."""
        def print(*args, **kwargs):
            if print_messages:
                return __builtins__.print(*args, **kwargs)
        try:
            with pyodbc.connect(settings.LAB_IMPORT_DMIS_DATA_SOURCE) as cnxn:
                with cnxn.cursor() as self.cursor:
                    for received_datetime, edc_specimen_identifier in self.received_items:
                        try:
                            packing_list_item = PackingListItem.objects.get(
                                item_reference=edc_specimen_identifier, received=False)
                            self.update_packing_list_item(packing_list_item, received_datetime)
                            print(edc_specimen_identifier + ' (received)')
                        except MultipleObjectsReturned:
                            for packing_list_item in PackingListItem.objects.filter(
                                    item_reference=edc_specimen_identifier, received=False):
                                self.update_packing_list_item(packing_list_item, received_datetime)
                                print(edc_specimen_identifier + ' (received - dup)')
                        except PackingListItem.DoesNotExist:
                            pass
                    for received_datetime, edc_specimen_identifier, alpha_code in self.stored_items:
                        try:
                            packing_list_item = PackingListItem.objects.get(
                                item_reference=edc_specimen_identifier, received=False)
                            Aliquot.objects.get(
                                aliquot_identifier=edc_specimen_identifier, aliquot_type__alpha_code=alpha_code)
                            self.update_packing_list_item(packing_list_item, received_datetime)
                            print(edc_specimen_identifier + ' (received in storage)')
                        except MultipleObjectsReturned:
                            for packing_list_item in PackingListItem.objects.filter(
                                    item_reference=edc_specimen_identifier, received=False):
                                self.update_packing_list_item(packing_list_item, received_datetime)
                                print(edc_specimen_identifier + ' (received in storage - dup)')
                        except PackingListItem.DoesNotExist:
                            pass
                        except Aliquot.DoesNotExist:
                            print(edc_specimen_identifier + ' Wrong specimen type. Got {}.'.format(alpha_code))
        except pyodbc.Error as error:
            if exception_cls:
                raise exception_cls(str(error))
            else:
                raise
        print('Received packing list items for {}:'.format(
            site_mappers.get_mapper(site_mappers.current_community).map_area, PackingListItem.objects.filter(received=True).count()))
        for panel in PackingListItem.objects.values('panel__name').filter(received=True).annotate(Count('panel')):
            print('{}: {}'.format(panel.get('panel__name'), panel.get('panel__count')))
        print('List of pending packing list items for {}:'.format(site_mappers.get_mapper(site_mappers.current_community).map_area))
        for packing_list_item in PackingListItem.objects.filter(received=False).order_by('created'):
            try:
                item_datetime = packing_list_item.item_datetime.strftime('%Y-%m-%d')
            except AttributeError:
                item_datetime = None
            try:
                panel_name = packing_list_item.panel.name.replace(' ', '_')
            except AttributeError:
                panel_name = None
            print('{} {} pending {} {}'.format(
                packing_list_item.item_reference,
                packing_list_item.packing_list.timestamp,
                item_datetime,
                panel_name,
            ))
