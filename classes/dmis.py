import logging
import pyodbc
import re
from datetime import datetime

from django.conf import settings
from django.db.models import Max

from lab_receive.models import Receive
from lab_order.models import Order
from lab_panel.models import Panel
from lab_result.models import Result
from lab_result.models import ResultSource
from lab_result_item.models import ResultItem
from lab_test_code.models import TestCode, TestCodeGroup
#from lab_common.utils import AllocateResultIdentifier
from lab_aliquot.models import Aliquot
from lab_aliquot_list.models import AliquotType, AliquotCondition, AliquotMedium
from lab_patient.models import Patient
from lab_account.models import Account
from import_history import ImportHistory

from bhp_research_protocol.models import Protocol, Site, Location
from base_dmis import BaseDmis


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Dmis(BaseDmis):

    def __init__(self, lab_db, debug=False, **kwargs):
        self.debug = debug
        self.lab_db = lab_db
        self.dmis_data_source = settings.LAB_IMPORT_DMIS_DATA_SOURCE

    def import_from_dmis(self, **kwargs):
        """Fetches a result from receiving up to the result items.

        ..note:: DMIS has a relational problem with the receiving table LAB01 where multiple
            receiving records can exist for the same primary sample. To correct this on import,
            the receiving record is only imported once while other records (order, result, resultitem)
            are imported complete. Also, LAB21 is not really an order record but there is a 1-many
            relationship between LAB21 and LAB21ResponseQ001x0 which kind of makes it look like one
            even though it was not created by the user as an order. In this script, we create an order and
            a result instance with the same data (LAB21). Result item instances are attached to
            the result instance.
        """

        lock_name = kwargs.get('subject_identifier', None)
        if not lock_name:
            if 'LAB_LOCK_NAME' in dir(settings):
                lock_name = settings.LAB_LOCK_NAME
            else:
                lock_name = kwargs.get('protocol', None)
        import_history = ImportHistory(self.lab_db, lock_name)
        if import_history.start():
            # start with the receiving records. If a receiving record (LAB01) has not been modified
            # on the dmis, nothing further will happen to it nor any of its related data (order, result, resultitem, ...).
            dmis_receives = self._fetch_dmis_receive_rows(import_history, **kwargs)
            if dmis_receives:
                # some of the structure here is to limit the number of calls to the SQL Server
                rowcount = len(dmis_receives)
                already_received = []
                protocol = None
                sites = {}
                patients = {}
                panel_ids = {}
                accounts = {}
                for dmis_receive in dmis_receives:
                    # check for the lock and stop everything if not found
                    if not import_history.locked:
                        # lock was deleted by another user
                        break
                    rowcount -= 1
                    # create one receive record per sample (dmis may have more than one for
                    # the same sample!)
                    if not dmis_receive.receive_identifier in already_received:
                        # for each protocol, site or account check if it is in the list first.
                        # If not, fetch or create and add to the list.
                        already_received.append(dmis_receive.receive_identifier)
                        if not protocol:
                            protocol = self._fetch_or_create_protocol(dmis_receive.protocol_identifier)
                        if dmis_receive.site_identifier not in [site_identifier for site_identifier in sites.iterkeys()]:
                            sites[dmis_receive.site_identifier] = self._fetch_or_create_site(dmis_receive.site_identifier)
                        if dmis_receive.protocol_identifier not in [account_name for account_name in accounts.iterkeys()]:
                            accounts[dmis_receive.protocol_identifier] = self._fetch_or_create_account(dmis_receive.protocol_identifier)
                        # for a patient, just fetch or create, no need for a list
                        patients[dmis_receive.subject_identifier] = self._create_or_update_patient(
                            account=accounts[dmis_receive.protocol_identifier],
                            subject_identifier=dmis_receive.subject_identifier,
                            gender=dmis_receive.gender,
                            dob=dmis_receive.dob,
                            initials=dmis_receive.initials)
                        # gather everything needed to create a new Receive instance into rcv_row
                        rcv_row = self.get_receive_row_from_cursor(dmis_receive)
                        rcv_row.protocol = protocol
                        rcv_row.site = sites[dmis_receive.site_identifier]
                        rcv_row.patient = patients[dmis_receive.subject_identifier]
                        receive = self._create_or_update_receive(rcv_row, rowcount)
                        del rcv_row
                    # gather what is needed to create an order instance,
                    # note: dmis_receive has the order information in it as well
                    ord_row = self.get_order_row_from_cursor(dmis_receive)
                    # data model is receive -> aliquot -> order
                    ord_row.aliquot = self._create_or_update_aliquot(receive, dmis_receive.tid)
                    # determine the order.panel from tid or else panel_id
                    if dmis_receive.tid and dmis_receive.tid != '-9':
                        if dmis_receive.tid not in [tid for tid in panel_ids.iterkeys()]:
                            panel_ids[dmis_receive.tid] = self._fetch_or_create_panel(dmis_receive.panel_id, ord_row.tid)
                        ord_row.panel = panel_ids[dmis_receive.tid]
                    elif dmis_receive.panel_id and dmis_receive.panel_id != '-9':
                        if dmis_receive.panel_id not in [panel_id for panel_id in panel_ids.iterkeys()]:
                            panel_ids[dmis_receive.panel_id] = self._fetch_or_create_panel(dmis_receive.panel_id, ord_row.tid)
                        ord_row.panel = panel_ids[dmis_receive.panel_id]
                    else:
                        # this will cause an error
                        ord_row.panel = None
                    # force an order to be recreated on import from dmis by deleting the existing one on lis
                    Order.objects.using(self.lab_db).filter(aliquot__receive=receive).delete()
                    if not ord_row.order_identifier:
                        # create a PENDING order instance using the receive_identifier
                        # as the order_identifier. (Dmis has no corresponding record)
                        ord_row.order_identifier = dmis_receive.receive_identifier
                        order = self._create_or_update_order(ord_row)
                    else:
                        # delete the PENDING order instance created above. (Dmis created the
                        # order when the results became available.)
                        # Order.objects.using(self.lab_db).filter(order_identifier=dmis_receive.receive_identifier).delete()
                        # create the order using the dmis order_identifier
                        order = self._create_or_update_order(ord_row)
                        del ord_row
                        if order:
                            result, result_modified = self._create_or_update_result(order)
                            if result and result_modified:
                                # delete existing result items. The dmis is the master, so if
                                # an item is added or removed from dmis it must reflect
                                ResultItem.objects.using(self.lab_db).filter(result=result).delete()
                                resultitem_rows = self._fetch_dmis_resultitem_rows(result.order.order_identifier)
                                max_validation_datetime = None
                                max_validation_user = None
                                for ritem in resultitem_rows:
                                    result_item = self._create_or_update_resultitem(result, ritem)
                                    result_item = self._validate_result_item(result, result_item)
                                    if not max_validation_datetime:
                                        max_validation_datetime = result_item.validation_datetime
                                        max_validation_user = result_item.validation_username
                                    if result_item.validation_datetime:
                                        if max_validation_datetime < result_item.validation_datetime:
                                            max_validation_datetime = result_item.validation_datetime
                                            max_validation_user = result_item.validation_username
                                if max_validation_datetime and max_validation_user:
                                    self._release_result(result, max_validation_datetime, max_validation_user)
                                else:
                                    logger.info('    NOT RELEASING {0} resulted on {1}'.format(order.order_identifier, order.order_datetime.strftime("%Y-%m-%d")))

        import_history.finish()
        return None

    def fetch_or_create_testcode(self, code):
        try:
            test_code = TestCode.objects.using(self.lab_db).get(code__exact=code)
        except:
            test_code_group = TestCodeGroup.objects.using(self.lab_db).get(code__exact='000')
            TestCode.objects.using(self.lab_db).create(
                code=code,
                name=code,
                units='-',
                test_code_group=test_code_group,
                display_decimal_places=0,
                is_absolute='absolute',
                )
            test_code = TestCode.objects.using(self.lab_db).get(code__iexact=code)
        return test_code

    def _fetch_or_create_protocol(self, protocol_identifier):
        protocols = Protocol.objects.using(self.lab_db).values('pk').filter(protocol_identifier__iexact=protocol_identifier)
        if protocols:
            protocol = Protocol.objects.using(self.lab_db).get(protocol_identifier__iexact=protocol_identifier)
        else:
            protocol = Protocol.objects.using(self.lab_db).create(
                protocol_identifier=protocol_identifier,
                research_title='unknown',
                short_title='unknown',
                local_title='unknown',
                date_registered=datetime.today(),
                date_opened=datetime.today(),
                description='auto created / imported from DMIS')
        return protocol

    def _fetch_or_create_account(self, account_name):
        accounts = Account.objects.using(self.lab_db).values('pk').filter(account_name__iexact=account_name)
        if accounts:
            account = Account.objects.using(self.lab_db).get(account_name__iexact=account_name)
        else:
            account = Account.objects.using(self.lab_db).create(
                account_name=account_name,
                account_opendate=datetime.today(),
                account_closedate=datetime.today(),
                user_created='auto',
                created=datetime.today(),
                comment='auto created / imported from DMIS')
        return account

    def _fetch_or_create_panel(self, panel_id, tid):
        """ Determines the panel given a tid or panel_id."""
        if panel_id == '-9':
            panel_id = None
        if tid == '-9':
            tid = None
        panel = None
        if tid:
            panels = Panel.objects.using(self.lab_db).filter(panel_group__name__exact=tid).order_by('name')
            if panels:
                panel = panels[0]
                for p in panels:
                    if re.search(settings.PROJECT_NUMBER, panel.name):
                        panel = p
                        break
                if not panel:
                    if panel_id:
                        # try to get using row.panel_id
                        panels = Panel.objects.using(self.lab_db).filter(dmis_panel_identifier=panel_id)
                        if panels:
                            panel = panels[0]
                            for p in panels:
                                if re.search(settings.PROJECT_NUMBER, panel.name):
                                    panel = p
                                    break
        if not panel:
            raise TypeError('Could not determine panel for tid={tid} '
                            'or panel_id={panel_id} protocol '
                            '{protocol}. Perhaps add one.'.format(tid=tid, panel_id=panel_id,
                                                protocol=settings.PROJECT_NUMBER))
        logger.info('      panel is {panel} from tid={tid} or panel_id={panel_id}'.format(panel=panel.name, tid=tid, panel_id=panel_id))
        return panel

    def _fetch_or_create_resultsource(self, **kwargs):
        interfaces = ['psm_interface', 'cd4_interface', 'auto', 'manual_entry', 'direct_import', ]
        agg = ResultSource.objects.using(self.lab_db).aggregate(Max('display_index'),)
        display_index = 0
        if agg:
            display_index = agg['display_index__max'] or 0
        # populate if not already ...
        for interface in interfaces:
            if not ResultSource.objects.using(self.lab_db).filter(name__iexact=interface):
                result_source = ResultSource.objects.using(self.lab_db).create(
                    name=interface,
                    short_name=interface,
                    display_index=display_index + 10,
                    )
        # create a new one if given argument and does not exist already
        if kwargs.get('interface'):
            if not ResultSource.objects.using(self.lab_db).filter(name__iexact=kwargs.get('interface')):
                result_source = ResultSource.objects.using(self.lab_db).create(
                    name=kwargs.get('interface'),
                    short_name=kwargs.get('interface'),
                    display_index=display_index + 11,
                    )
            else:
                result_source = ResultSource.objects.using(self.lab_db).get(name__iexact=kwargs.get('interface'))
        else:
            result_source = None
        return result_source

    def _fetch_or_create_site(self, site_identifier):
        if site_identifier == None or site_identifier == '' or site_identifier == '-9':
            site_identifier = '00'
        sites = Site.objects.using(self.lab_db).values('pk').filter(site_identifier__iexact=site_identifier)
        if sites:
            site = Site.objects.using(self.lab_db).get(site_identifier__iexact=site_identifier)
        else:
            location = Location.objects.using(self.lab_db).values('pk').filter(name__exact='UNKNOWN')
            if location:
                location = Location.objects.using(self.lab_db).get(name__exact='UNKNOWN')
            else:
                location = Location.objects.using(self.lab_db).create(name='UNKNOWN')
            site = Site.objects.using(self.lab_db).create(site_identifier=site_identifier, name=site_identifier, location=location)
        return site

    def _create_or_update_receive(self, row, rowcount):
        #is this receiving record on file
        if Receive.objects.using(self.lab_db).values('pk').filter(receive_identifier=row.receive_identifier).exists():
            # force overwrite by not checking modified date on local receive -- local edits are overwritten.
            receive = Receive.objects.using(self.lab_db).get(receive_identifier=row.receive_identifier)
#                if receive.modified < row.modified:
            receive.patient = row.patient
            receive.modified = row.modified
            receive.user_modified = row.user_modified
            receive.protocol = row.protocol
            receive.drawn_datetime = row.drawn_datetime
            receive.receive_datetime = row.receive_datetime
            receive.site = row.site
            receive.visit = row.visit
            receive.clinician_initials = row.clinician_initials
            receive.dmis_reference = row.dmis_reference
            receive.requisition_identifier = row.edc_specimen_identifier or row.other_pat_ref
            receive.receive_condition = row.condition
            receive.save()
            logger.info('  dmis - receive: {rowcount} updating {receive_identifier} '
                        'for {subject_identifier}.'.format(rowcount=rowcount,
                                                           receive_identifier=row.receive_identifier,
                                                               subject_identifier=row.subject_identifier))
#                else:
#                    logger.info('  dmis - receive: {rowcount} found {receive_identifier} for '
#                                '{subject_identifier} (not modified).'.format(rowcount=rowcount,
#                                                               receive_identifier=row.receive_identifier,
#                                                               subject_identifier=row.subject_identifier))
        else:
            receive = Receive.objects.using(self.lab_db).create(
                protocol=row.protocol,
                receive_identifier=row.receive_identifier,
                patient=row.patient,
                site=row.site,
                visit=row.visit,
                drawn_datetime=row.drawn_datetime,
                receive_datetime=row.receive_datetime,
                user_created=row.user_created,
                user_modified=row.user_modified,
                created=row.created,
                modified=row.modified,
                dmis_reference=row.dmis_reference,
                clinician_initials=row.clinician_initials,
                requisition_identifier=row.edc_specimen_identifier or row.other_pat_ref,
                receive_condition=row.condition)
            logger.info('  dmis - receive: {rowcount} creating '
                        '{receive_identifier} for {subject_identifier}'.format(rowcount=rowcount,
                                                                               receive_identifier=row.receive_identifier,
                                                                               subject_identifier=row.subject_identifier))
        return receive

    def _create_or_update_order(self, row):
        if Order.objects.using(self.lab_db).filter(order_identifier=row.order_identifier):
            # order identifier is unique
            order = Order.objects.using(self.lab_db).get(order_identifier=row.order_identifier)
            if order.modified < row.modified:
                order.order_identifier = row.order_identifier
                order.order_datetime = row.order_datetime
                order.aliquot = row.aliquot
                status = 'COMPLETE'
                order.panel = row.panel
                order.comment = '',
                order.created = row.created
                order.modified = row.modified
                order.user_created = row.user_created
                order.user_modified = row.user_modified
                order.dmis_reference = row.dmis_reference
                order.save()
                logger.info('    order: updated {order_identifier} {panel}'.format(order_identifier=row.order_identifier, panel=row.panel.name))
            else:
                logger.info('    order: found {order_identifier} {panel} (not modified)'.format(order_identifier=row.order_identifier, panel=row.panel.name))
        elif Order.objects.using(self.lab_db).filter(order_identifier=row.receive_identifier):
            # update PENDING order previously created by django-lis identified by the receive_identifier
            order = Order.objects.using(self.lab_db).get(order_identifier=row.receive_identifier)
            order.order_identifier = row.order_identifier
            order.order_datetime = row.order_datetime
            order.aliquot = row.aliquot
            status = 'COMPLETE'
            order.panel = row.panel
            order.comment = '',
            order.created = row.created
            order.modified = row.modified
            order.user_created = row.user_created
            order.user_modified = row.user_modified
            order.dmis_reference = row.dmis_reference
            order.save()
            logger.info('    order: updated pending {receive_identifier} {panel}. '
                        'order_identifier is now {order_identifier}'.format(receive_identifier=row.receive_identifier,
                                                                                  order_identifier=row.order_identifier,
                                                                                  panel=row.panel.name))
        else:
            if row.receive_identifier == row.order_identifier:
                status = 'PENDING'
            else:
                status = 'COMPLETE'
            order = Order.objects.using(self.lab_db).create(
                order_identifier=row.order_identifier,
                order_datetime=row.order_datetime,
                aliquot=row.aliquot,
                status=status,
                panel=row.panel,
                comment='',
                created=row.created,
                modified=row.modified,
                user_created=row.user_created,
                user_modified=row.user_modified,
                dmis_reference=row.dmis_reference,
                )
            logger.info('    order: created {order_identifier} {panel}'.format(order_identifier=row.order_identifier, panel=row.panel.name))
        return order

    def _create_or_update_result(self, order):
        """ Updates the dmis result using the given \'order\' by querying the dmis server on the order_identifier for
        a dmis result (LAB21) that has result_items (LAB21D)"""
        result = None
        result_is_modified = False
        cnxn2 = pyodbc.connect(self.dmis_data_source)
        cursor = cnxn2.cursor()
        sql = ('select distinct headerdate as result_datetime, '
           'l21.keyopcreated as user_created, '
           'l21.keyoplastmodified as user_modified, '
           'l21.datecreated as created, '
           'l21.datelastmodified as modified, '
           'convert(varchar(36), l21.result_guid) as result_guid '
           'from BHPLAB.DBO.LAB21Response as L21 '
           'left join BHPLAB.DBO.LAB21ResponseQ001X0 as L21D on L21.Q001X0=L21D.QID1X0 '
           'where l21.id=\'{order_identifier}\' and '
           'l21d.id is not null').format(order_identifier=order.order_identifier)
        # cursor.execute(str(sql))
        # on dmis exists, same as django - do nothing
        # on dmis exists, older on django - update
        # on dmis was deleted, still exists on django - delete
        # on dmis exists, not on dkjango  - create
        if not cursor.execute(str(sql)).fetchone():
            # there is an order with no result (that is, no result items l21d.id is null)
            logger.warning('    result: no result on source for order {order_identifier}'.format(order_identifier=order.order_identifier))
            for result in Result.objects.using(self.lab_db).filter(order=order):
                result.delete()
                logger.warning('    result: deleted from target for order {order_identifier}'.format(order_identifier=order.order_identifier))
                result_is_modified = True  # ??
        else:
            # most likely just one row
            for row in cursor.execute(str(sql)):
                if Result.objects.using(self.lab_db).filter(order=order):
                    # result identifier is unique and an order should only have one result
                    result = Result.objects.using(self.lab_db).get(order=order)
                    if result.modified < row.modified:
                        #result.result_identifier = result_identifier, # allocated by django-lis
                        #result.order = order,
                        result.result_datetime = row.result_datetime
                        result.comment = ''
                        result.user_created = row.user_created
                        result.user_modified = row.user_modified
                        result.created = row.created
                        result.modified = row.modified
                        result.dmis_result_guid = row.result_guid
                        result.save()
                        result_is_modified = True
                        logger.info('    result: updated {result_identifier}'.format(result_identifier=result.result_identifier))
                    else:
                        result_is_modified = False
                        logger.info('    result: found {result_identifier} (not modified)'.format(result_identifier=result.result_identifier))
                else:
                    result = Result.objects.using(self.lab_db).create(
                        order=order,
                        result_datetime=row.result_datetime,
                        comment='',
                        user_created=row.user_created,
                        user_modified=row.user_modified,
                        created=row.created,
                        modified=row.modified,
                        dmis_result_guid=row.result_guid)
                    result_is_modified = True
                    #self._fetch_or_create(ResultSource)
                    logger.info('    result: created {result_identifier}'.format(result_identifier=result.result_identifier))
        return result, result_is_modified

    def _create_or_update_resultitem(self, result, ritem, delete=False):
        """ Creates a result item for the given ritem from the dmis.

        ..note:: dmis item overwrites and existing django-lis item. The dmis sql statement is
        ordered on datelastmodified which means oldest testcodes will come in first
        and later be overwritten by the same testcode if a testcode appears more than once for a result.
        """

        def get_ritem_user(dmis_user):
            # change NT system username to auto
            if dmis_user.strip(' \t\n\r').upper() == 'NT AUTHORITY\SYSTEM':
                user = 'auto'
            else:
                user = dmis_user
            return user

        def get_ritem_validation(ritem):
            result_item_source = ''
            result_item_source_reference = ''
            validation_reference = ''
            # evaluate validation_reference
            if ritem.validation_reference == '-9':
                # this is an item from GetResults TCP connected to PSM
                result_item_source = self._fetch_or_create_resultsource(interface='psm_interface')
                result_item_source_reference = ''
                validation_reference = 'dmis-auto'
            elif ritem.validation_reference == 'LAB21:MANUAL':
                # manual entry and no validation -- straight to LAB21 tableset
                result_item_source = self._fetch_or_create_resultsource(interface='manual_entry')
                result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                validation_reference = 'auto'
            elif re.search('^rad[0-9A-F]{5}\.tmp$', ritem.validation_reference):
                # this is an item from GetResults Flatfile and validated via the LAB05 path
                result_item_source = self._fetch_or_create_resultsource(interface='cd4_interface')
                result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                validation_reference = 'lab05'
            elif re.search('^LAB23:', ritem.validation_reference):
                # manual entry and validated via the LAB23 validation path
                result_item_source = self._fetch_or_create_resultsource(interface='manual_entry')
                result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                validation_reference = 'lab23'
            elif re.search('^IMPORT', ritem.validation_reference):
                # manual entry and validated via the LAB23 validation path
                result_item_source = self._fetch_or_create_resultsource(interface='direct_import')
                result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                validation_reference = 'auto'
            elif re.search('^LB003:', ritem.validation_reference):
                # manual import
                result_item_source = self._fetch_or_create_resultsource(interface='direct_import')
                result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                validation_reference = 'auto'
            elif re.search('^LB004:', ritem.validation_reference):
                # manual import
                result_item_source = self._fetch_or_create_resultsource(interface='direct_import')
                result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                validation_reference = 'auto'
            elif re.search('^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$', ritem.validation_reference):
                # manual import
                result_item_source = self._fetch_or_create_resultsource(interface='manual_entry')
                result_item_source_reference = 'dmis-%s' % ritem.validation_reference
                validation_reference = 'auto'
            else:
                # missed a case? let's hear about it
                raise TypeError('Validation reference \'%s\' was not expected. See dmis_fetch_result.' % ritem.validation_reference)
            result_item_source_reference = '%s %s' % (result_item_source_reference, ritem.mid)
            return {'validation_reference': validation_reference,
                    'result_item_source': result_item_source,
                    'result_item_source_reference': result_item_source_reference}

        code = ritem.code.strip(' \t\n\r')
        # usually delete all items as soon as the result instance is known.
        if delete:
            # delete from django-lis the one result item for this result (should only be one)
            ResultItem.objects.using(self.lab_db).filter(result=result, test_code__code=code).delete()
        test_code = self.fetch_or_create_testcode(code)
        user = get_ritem_user(ritem.user_created)
        validation = get_ritem_validation(ritem)
        # create a new result item. set validation to 'P', we'll import
        # full validation information later
        result_item = ResultItem.objects.using(self.lab_db).create(
            result=result,
            test_code=test_code,
            result_item_datetime=ritem.result_item_datetime,
            result_item_value=ritem.result_value,
            result_item_quantifier=ritem.result_quantifier,
            validation_status='P',
            validation_reference=validation['validation_reference'],
            result_item_source=validation['result_item_source'],
            result_item_source_reference=validation['result_item_source_reference'],
            result_item_operator=user,
            comment='',
            )
        logger.info('      created item {0}'.format(code, ritem.result_item_datetime.strftime("%Y-%m-%d")))
        return result_item

    def _create_or_update_patient(self, **kwargs):
        subject_identifier = kwargs.get('subject_identifier').strip(' \t\n\r')
        initials = kwargs.get('initials').strip(' \t\n\r')
        if not initials:
            initials = 'X0X'
        account = kwargs.get('account')
        gender = kwargs.get('gender')
        dob = kwargs.get('dob')
        is_dob_estimated = '-'
        patients = Patient.objects.using(self.lab_db).values('pk').filter(subject_identifier__iexact=subject_identifier)
        if patients:
            patient = Patient.objects.using(self.lab_db).get(subject_identifier__iexact=subject_identifier)
            patient.dob = dob
            patient.gender = gender
            patient.is_dob_estimated = is_dob_estimated
            patient.initials = initials
            patient.save()
        else:
            patient = Patient.objects.using(self.lab_db).create(
                subject_identifier=subject_identifier,
                initials=initials,
                gender=gender,
                dob=dob,
                is_dob_estimated=is_dob_estimated,
                comment='auto created / imported from DMIS')
            patient.account.add(account)
        return patient

    def _create_or_update_aliquot(self, receive, tid):

        if receive.receive_condition:
            aliquot_condition = self._create_or_update_aliquotcondition(receive.receive_condition)
        else:
            aliquot_condition = None
        #create primary
        # TODO: need more detail here for sample types other than the ones listed here...
        create = {}
        if tid == '411':
            create['type'] = '02'  # WB
            create['medium'] = 'DBS'
        else:
            create['type'] = '02'  # WB
            create['medium'] = 'TUBE'
        # get or create the primary aliquot
        aliquot_identifier = '%s0000%s01' % (receive.receive_identifier, create['type'])
        if Aliquot.objects.using(self.lab_db).values('pk').filter(aliquot_identifier__iexact=aliquot_identifier):
            primary_aliquot = Aliquot.objects.using(self.lab_db).get(aliquot_identifier__iexact=aliquot_identifier)
            if not primary_aliquot.modified == receive.modified:
                aliquot_type = AliquotType.objects.using(self.lab_db).get(numeric_code__exact=create['type'])
                primary_aliquot.modified = receive.modified
                primary_aliquot.aliquot_type = aliquot_type
                primary_aliquot.aliquot_condition = aliquot_condition
                primary_aliquot.save()
        else:
            create['comment'] = 'auto created on import from DMIS'
            aliquot_type = AliquotType.objects.using(self.lab_db).get(numeric_code__exact=create['type'])
            aliquot_medium = AliquotMedium.objects.using(self.lab_db).get(short_name__iexact=create['medium'])
            primary_aliquot = Aliquot.objects.using(self.lab_db).create(
                aliquot_identifier=aliquot_identifier,
                receive=receive,
                count=1,
                aliquot_type=aliquot_type,
                medium=aliquot_medium,
                aliquot_condition=aliquot_condition,
                comment=create['comment'],
                )
        return primary_aliquot

    def _create_or_update_aliquotcondition(self, condition):
        if AliquotCondition.objects.using(self.lab_db).values('pk').filter(short_name__exact=condition):
            aliquot_condition = AliquotCondition.objects.using(self.lab_db).get(short_name__exact=condition)
        else:
            agg = AliquotCondition.objects.using(self.lab_db).aggregate(Max('display_index'),)
            if not agg:
                display_index = 10
            else:
                display_index = agg['display_index__max'] + 10
            aliquot_condition = AliquotCondition.objects.using(self.lab_db).create(
                name=condition,
                short_name=condition,
                display_index=display_index,
                )
        return aliquot_condition

    def _validate_result_item(self, result, result_item, **kwargs):
        """ Imports result item validation information from the dmis.

        ..note:: For legacy reasons, dmis has more than one approach to capturing validation information. For
        CD4 results the LAB05 path is used, while for all other results the LAB23 path id used. Additionally, for
        results that are auto validated, like those coming from PSM, the information comes from LAB21 directly.
        """
        def _validate_l21(result_item, result):
            result_item.result_item_operator = result.user_created.strip('BHP\\bhp\\')
            result_item.validation_status = 'F'
            result_item.validation_datetime = result_item.result_item_datetime or result_item.validation_datetime
            result_item.validation_username = 'auto'
            result_item.save()

        def _validate_l23(result_item, row):
            result_item.result_item_operator = row.operator.strip('BHP\\bhp\\')
            result_item.validation_status = 'F'
            result_item.validation_datetime = row.validation_datetime
            result_item.validation_username = row.validation_username.strip('BHP\\bhp\\')
            result_item.save()

        def _validate_l5(result_item, row):
            _validate_l23(result_item, row)

        cnxn2 = pyodbc.connect(self.dmis_data_source)
        cursor_result = cnxn2.cursor()
        # if you know the 'interface' then you know how validation occurs
        cd4_interface = ResultSource.objects.using(self.lab_db).get(name__iexact='cd4_interface')
        psm_interface = ResultSource.objects.using(self.lab_db).get(name__iexact='psm_interface')
        direct_interface = ResultSource.objects.using(self.lab_db).get(name__iexact='direct_import')
        manual_interface = ResultSource.objects.using(self.lab_db).get(name__iexact='manual_entry')
        #the validation process depends on the 'interface'.
        if result_item.result_item_source == psm_interface:
            _validate_l21(result_item, result)
        elif result_item.result_item_source == direct_interface:
            _validate_l21(result_item, result)
        elif result_item.result_item_source == cd4_interface:
            #this returns only one record per result, only, so update all items as one
            # hmmm ... all imported results are from LAB21 which implies result_accepted=1, add "where result_accepted=1"
            sql = ("select result_accepted_username as operator, "
                    "result_accepted_username as validation_username, "
                    "l5.result_accessed_date as validation_datetime "
                    "from bhplab.dbo.lab05response as l5 "
                    "left join bhplab.dbo.results_101 as r101 on l5.result_guid=r101.result_guid "
                    "where result_accepted=1 and convert(varchar(36),l5.result_guid)='%s'") % result.dmis_result_guid

            cursor_result = cnxn2.cursor()
            cursor_result.execute(str(sql))
            for row in cursor_result:
                _validate_l5(result_item, row)
        elif result_item.result_item_source == manual_interface and result_item.validation_reference.lower() != 'lab23':
            _validate_l21(result_item, result)
        elif result_item.result_item_source == manual_interface and result_item.validation_reference.lower() == 'lab23':
            #this returns one record per result, only, so update all items as one
            sql = ('select lower(L23.operator) as operator, '
                   'lower(l23d.checkbatch_user) as validation_username, '
                   'l23d.datelastmodified as validation_datetime, '
                   'convert(varchar, l23.id) as validation_reference '
                   'from bhplab.dbo.lab23response as l23 '
                   'left join bhplab.dbo.lab23responseq001x0 as l23d on l23.q001x0=l23d.qid1x0 '
                   'where result_accepted=1 and upper(ltrim(rtrim(utestid)))=\'{code}\' and '
                   'convert(varchar(36),result_guid)=\'{result_guid}\'').format(code=result_item.test_code.code,
                                                                                result_guid=result.dmis_result_guid)
            cursor_result = cnxn2.cursor()
            cursor_result.execute(str(sql))
            for row in cursor_result:
                _validate_l23(result_item, row)
        else:
            raise TypeError('Unknown case result_item_source in dmis validation. '
                            'Got \'%s\' from result %s.' % (result.resultitem.result_item_source, result))
        logger.info('      validated item %s %s (%s)' % (result_item.test_code.code, result_item.result_item_source, result_item.validation_status))
        return result_item

    def _release_result(self, result, validation_datetime, validation_username, **kwargs):

        if not validation_datetime:
            raise TypeError('Expected a date for validation_datetime for '
                            'result {0}. Got None.'.format(result.result_identifier))
        elif validation_username == 'auto' or not validation_username:
            validation_username = unicode('smoyo')
        # remove oldest of any duplicate result_items

        # update result
        result.release_status = 'RELEASED'
        result.release_datetime = validation_datetime
        result.release_username = validation_username
        result.save()
        logger.info('      released by {validation_username} on '
                    '{validation_datetime}'.format(validation_username=validation_username,
                                                   validation_datetime=validation_datetime))

    def _fetch_dmis_receive_rows(self, import_history, **kwargs):

        def _get_dmis_receive_where_clause(clause=None, **kwargs):
            subject_identifier = kwargs.get('subject_identifier', None)
            protocol = kwargs.get('protocol', None)
            where_clause = []
            if import_history.clause:
                where_clause.append(import_history.clause)
            if subject_identifier:
                where_clause.append('l.pat_id like \'%{subject_identifier}%\''.format(subject_identifier=subject_identifier))
            if protocol:
                where_clause.append('sample_protocolnumber=\'{protocol}\''.format(protocol=protocol))
            if where_clause:
                where_clause = 'where {0}'.format(' and '.join(where_clause))
            else:
                where_clause = ''
            return where_clause

        subject_identifier = kwargs.get('subject_identifier', None)
        protocol = kwargs.get('protocol', None)
        cnxn = pyodbc.connect(self.dmis_data_source)
        cursor = cnxn.cursor()
        where_clause = _get_dmis_receive_where_clause(import_history.clause, **kwargs)
        if where_clause is None:
            where_clause = ''
        sql = ('select '
               'l.id as dmis_reference,'
                'l.pid as receive_identifier, '
                'l.tid, '
                'l.sample_condition,'
                'l.sample_visitid as visit,'
                'l.sample_site_id as site_identifier,'
                'l.sample_protocolnumber as protocol_identifier,'
                'l.gender,'
                'dob as dob,'
                'l.pat_id as subject_identifier,'
                'l.pinitials as initials, '
                'l.cinitials as clinician_initials, '
                'l.keyopcreated as user_created,'
                'l.keyoplastmodified as user_modified,'
                'l.headerdate as receive_datetime, '
                'l.sample_date_drawn as drawn_datetime,'
                'l.datecreated as created, '
               ' l.datelastmodified as modified,'
                'l21.id as order_identifier,'
                'l21.panel_id, '
                'l.edc_specimen_identifier, '
                'l.other_pat_ref '
                'from lab01response as l '
                'left join lab21response as l21 on l.pid=l21.pid '
                ' {where_clause} '
                'order by l.pat_id, l.datelastmodified desc').format(where_clause=where_clause)
        rows = cursor.execute(str(sql)).fetchall()
        if len(rows) == 0:
            logger.info('  dmis - receive: nothing received for {subject_identifier}'
                        '{protocol} since '
                        '{last_import_datetime}.'.format(subject_identifier=subject_identifier or '',
                                                   protocol=protocol or '',
                                                   dmis_data_source='lab',
                                                   last_import_datetime=import_history.last_import_datetime))
        return rows

    def _fetch_dmis_resultitem_rows(self, order_identifier):
        # get list of result items for this result from DMIS (LAB21ResponseQ001X0)
        # order by datelastmodified so that if there is more than one value for a
        # testcode, the youngest will overwrite the older ones.
        cnxn3 = pyodbc.connect(self.dmis_data_source)
        cursor_resultitem = cnxn3.cursor()
        sql = ('select l21d.sample_assay_date, '
                'utestid as code,'
                'result as result_value, '
                'result_quantifier, '
                'status, '
                'mid,'
                'l21d.validation_ref as validation_reference, '
                'l21d.datelastmodified as result_item_datetime, '
                'l21d.keyopcreated as user_created, '
                'l21d.keyoplastmodified as user_modified, '
                'l21.datecreated as created, '
                'l21.datelastmodified as modified '
                'from BHPLAB.DBO.LAB21Response as L21 '
                'left join BHPLAB.DBO.LAB21ResponseQ001X0 as L21D on L21.Q001X0=L21D.QID1X0 '
                'where l21.id=\'%s\' and l21d.id is not null and l21d.result<>\'*\' order by l21d.datelastmodified') % order_identifier
        return cursor_resultitem.execute(str(sql))
