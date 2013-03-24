import logging
import os
import sqlite3
import subprocess
from datetime import datetime
from tastypie.models import ApiKey
from django.db.models import Model
from django.conf import settings
from django.db.models import signals
from bhp_common.utils import td_to_string
from bhp_base_model.models import BaseModel
from bhp_sync.models import BaseSyncUuidModel
from bhp_base_model.models import BaseUuidModel
from lab_base_model.models import BaseLabUuidModel
from bhp_consent.models.signals import add_models_to_catalogue
from base_prepare_device import BasePrepareDevice
from bhp_dispatch.exceptions import BackupError, RestoreError
from lab_base_model.models import BaseLabListModel, BaseLabModel


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class PrepareDevice(BasePrepareDevice):

    def __init__(self, using_source,
                  using_destination,
                  **kwargs):
        """
        Args:
            using_source: settings database key for the source.
            using_destination: settings database key for the destination.
        Keywords:
            exception: exception class to use, e.g. CommandError if this is run as a management command. Default(TypeError)
        """
        super(PrepareDevice, self).__init__(using_source, using_destination, **kwargs)
        self.started = None
        self.start_time = None
        self.end_time = None

    def timer(self, done=None):
        if not self.started:
            self.started = datetime.today()
            logger.info('Starting at {0}'.format(self.started))
        self._end_timer()
        self.start_time = datetime.today()
        if done:
            logger.info("processed in {0}".format(td_to_string(datetime.today() - self.started)))

    def _end_timer(self):
        if self.start_time:
            logger.info("    ....processed in {0}".format(td_to_string(datetime.today() - self.start_time)))

    def pre_prepare(self):
        return None

    def post_prepare(self):
        return None

    def prepare(self, **kwargs):
        """Runs for all common data needed for an EDC installation.

        Keywords:
            step: if specified skip to the numbered step. default(0)
        """
        # check for outgoing transactions first
        if self.has_outgoing_transactions():
            raise self.exception("Destination has outgoing transactions. Please sync and try again.")
        step = int(kwargs.get('step', 0))
        logger.info('Starting at step {0}'.format(step))
        if not step > 1:
            self.timer()
            logger.info("1. Running pre procedures")
            self.pre_prepare()
        if not step > 2:
            self.timer()
            logger.info("2. Updating content_type")
            self.update_content_type()
        if not step > 3:
            self.timer()
            logger.info("3. Updating auth...")
            self.update_auth()
        if not step > 4:
            self.timer()
            logger.info("4. Updating api keys...")
            self.update_model(ApiKey, [Model])
        if not step > 5:
            self.timer()
            logger.info("5. Updating lists...")
            self.update_list_models()
        if not step > 6:
            self.timer()
            logger.info("6. Updating bhp variables...")
            self.update_app_models('bhp_variables', [BaseUuidModel])
        if not step > 7:
            self.timer()
            logger.info("7. Updating contenttypemap...")
            logger.info('    ...update')
            self.update_app_models('bhp_content_type_map', [BaseModel])
            logger.info('    ...resize')
            self.resize_content_type()
            self.update_app_models('bhp_content_type_map', [BaseModel])
            logger.info('    ...pop and sync')
            self.sync_content_type_map()
        if not step > 8:
            self.timer()
            logger.info("8. Updating appointment configuration...")
            self.update_model(("bhp_appointment", "Configuration"), [BaseSyncUuidModel])
        if not step > 9:
            self.timer()
            logger.info("9. Updating the Crypt table...")
            #self.update_model(('bhp_crypto', 'crypt'))
            logger.info('   Warning, skipping. use mysqldump for the Crypt table, bhp_crypto_crypt')
        if not step > 10:
            self.timer()
            logger.info("10. Updating the visit definitions...")
            self.update_app_models('bhp_visit', [BaseUuidModel])
        if not step > 11:
            self.timer()
            logger.info("11. Updating subject identifiers...")
            self.update_app_models('bhp_identifier', [BaseModel])
        if not step > 12:
            self.timer()
            logger.info("12. Updating registered subjects...")
            #self.update_model(('bhp_registration', 'RegisteredSubject'), [RegisteredSubject])
            logger.info('   Warning, skipping. use mysqldump for the RegisteredSubject table, bhp_registration_registeredsubject')
        if not step > 13:
            self.timer()
            logger.info("13. Updating bhp_consent Consent Catalogues...")
            signals.post_save.disconnect(add_models_to_catalogue, weak=False, dispatch_uid="add_models_to_catalogue")
            self.update_model(('bhp_consent', 'ConsentCatalogue'), [BaseSyncUuidModel])
        if not step > 14:
            self.timer()
            logger.info("14. Updating bhp_consent Attached Models...")
            #self.update_model(('bhp_consent', 'AttachedModel'), [BaseSyncUuidModel])
            signals.post_save.connect(add_models_to_catalogue, weak=False, dispatch_uid="add_models_to_catalogue")
        if not step > 15:
            self.timer()
            logger.info("15. Updating lab test code groups from lab_test_code...")
            self.update_model(('lab_test_code', 'TestCodeGroup'), [BaseLabListModel, BaseLabModel])
        if not step > 16:
            self.timer()
            logger.info("16. Updating lab test codes from lab_test_code...")
            self.update_model(('lab_test_code', 'TestCode'), [BaseLabListModel, BaseLabModel])
        if not step > 17:
            self.timer()
            logger.info("17. Updating lab aliquot types from lab_aliquot_list...")
            self.update_model(('lab_aliquot_list', 'AliquotType'), [BaseModel])
        if not step > 18:
            self.timer()
            logger.info("18. Updating lab panel models from lab_panel...")
            self.update_app_models('lab_panel', [BaseModel])
        if not step > 19:
            self.timer()
            logger.info("19. Updating aliquot types from lab_clinic_api...")
            self.update_model(('lab_clinic_api', 'AliquotType'), [BaseLabListModel, BaseLabModel])
        if not step > 20:
            self.timer()
            logger.info("20. Updating test code groups from lab_clinic_api...")
            self.update_model(('lab_clinic_api', 'TestCodeGroup'), [BaseLabListModel, BaseLabModel])
        if not step > 21:
            self.timer()
            logger.info("21. Updating test codes from lab_clinic_api...")
            self.update_model(('lab_clinic_api', 'TestCode'), [BaseLabListModel, BaseLabModel])
        if not step > 22:
            self.timer()
            logger.info("22. Updating panel from lab_clinic_api...")
            self.update_model(('lab_clinic_api', 'Panel'), [BaseLabListModel, BaseLabModel])
        if not step > 23:
            self.timer()
            logger.info("23. Updating review from lab_clinic_api...")
            self.update_model(('lab_clinic_api', 'Review'), [BaseLabUuidModel])
        if not step > 24:
            self.timer()
            logger.info("24. Updating un-scheduled lab entry buckets from bhp_lab_entry...")
            self.update_model(('bhp_lab_entry', 'UnscheduledLabEntryBucket'))
        if not step > 25:
            self.timer()
            logger.info("25. Updating lab entry from bhp_lab_entry...")
            self.update_model(('bhp_lab_entry', 'LabEntry'), [BaseUuidModel])
        if not step > 26:
            self.timer()
            logger.info("26. Updating bhp_entry.models.entry...")
            self.update_model(('bhp_entry', 'entry'), [BaseUuidModel])
        if not step > 27:
            self.timer()
            logger.info("27. Updating api keys...")
            self.update_api_keys()
        if not step > 28:
            self.timer()
            logger.info("28. Running post procedures...")
            self.post_prepare()
        logger.info("Done")
        self.timer(done=True)

    def backup_database(self, **kwargs):
        """Takes a backup of the netbook before preparing a netbook for dispatch"""
        #Check if were on the server or netbook
        fname = None
        if not settings.DEVICE_ID == self.server_device_id:
            raise TypeError('DB Snapshot must be done from the server.')
        if self._get_db_engine() == 'mysql':
            fname = self._backup_mysql_database()
        if self._get_db_engine() == 'sqlite3':
            fname = self._backup_sqlite3_database()
        if not fname:
            raise self.exception("DB Snapshot failed, unable to backup {0} database for {1}.".format(self._get_db_engine(), self.get_using_destination()))
        return fname

    def _backup_sqlite3_database(self):
        db = "{0}.db".format(self.get_using_destination())
        fd = self._get_backup_file_handle()
        con = sqlite3.connect("{0}.db".format(db))
        for row in con.execute('PRAGMA database_list;'):
            command_list = ['sqlite3', row[2], '.dump']
            if subprocess.Popen(command_list, stdout=fd).returncode:
                raise BackupError('Unable to backup. Tried with {0}'.format(command_list))
        return fd.name

    def _backup_mysql_database(self):
        db_user = settings.DATABASES[self.get_using_destination()]['USER']
        db_pass = settings.DATABASES[self.get_using_destination()]['PASSWORD']
        db = settings.DATABASES[self.get_using_destination()]['NAME']
        fd = self._get_backup_file_handle()
        command_list = ['mysqldump', '-u', db_user, '-p{0}'.format(db_pass), db]
        if subprocess.Popen(command_list, stdout=fd).returncode:
            raise BackupError('Unable to backup. Tried with {0}'.format(command_list))
        return fd.name

    def _restore_sqlite3_database(self):
        db = "{0}.db".format(self.get_using_destination())
        fd = open(self._get_last_backup_filename(), 'wb')
        con = sqlite3.connect("{0}.db".format(db))
        for row in con.execute('PRAGMA database_list;'):
            command_list = ['sqlite3', fd.name, '.restore']
            if subprocess.Popen(command_list, stdin=fd).returncode:
                raise BackupError('Unable to restore. Tried with {0}'.format(command_list))
        return fd.name

    def _restore_mysql_database(self, destination_host=None):
        db_user = settings.DATABASES[self.get_using_destination()]['USER']
        db_pass = settings.DATABASES[self.get_using_destination()]['PASSWORD']
        db = settings.DATABASES[self.get_using_destination()]['NAME']
        if not destination_host:
            destination_host = settings.DATABASES[self.get_using_destination()]['HOST']
        fd = self._get_backup_file_handle()
        command_list = ['mysql', '-h', destination_host, '-u', db_user, '-p{0}'.format(db_pass), db]
        if subprocess.Popen(command_list, stdin=fd).returncode:
            raise BackupError('Unable to restore. Tried with {0}'.format(command_list))
        return fd.name

    def _get_backup_file_handle(self):
        return open(self._get_next_backup_filename(), 'wb')

    def _get_next_backup_filename(self):
        return os.path.join(self._get_backup_path(), '{0}-{1}.sql'.format(self.get_using_destination(), datetime.today().strftime('%Y%m%d%H%M%S%f')))

    def _get_backup_path(self):
        """Returns the full path to the backup folder."""
        if not 'DB_SNAPSHOT_DIR' in dir(settings):
            backup_path = os.path.join(settings.DIRNAME, 'db_snapshots')
            if not os.path.exists(backup_path):
                subprocess.call(["mkdir", "-p", backup_path])
        else:
            backup_path = settings.DB_SNAPSHOT_DIR
            if not os.path.exists(backup_path):
                subprocess.call(["mkdir", "-p", backup_path])
        return backup_path

    def _get_db_engine(self):
        """Returns the database engine in use."""
        engine = settings.DATABASES[self.get_using_destination()]['ENGINE'].split('.')[-1:][0]
        if engine not in ['mysql', 'sqlite3']:
            raise TypeError('Unknown db engine. Got {0}'.format(engine))
        return engine

    def _get_last_backup_filename(self):
        """Returns the filename of the last backup for this destination."""
        last_filename = None
        # get list of files in backup path
        filenames = os.listdir(self._get_backup_path())
        if filenames:
            # remove any not starting in "destination"
            filenames = [filename for filename in filenames if filename.startswith(self.get_using_destination()) and filename.endswith('sql')]
            # if any items left, sort and pick the last one
            if filenames:
                filenames.sort()
                last_filename = os.path.join(self._get_backup_path(), filenames[-1:][0])
        return last_filename

    def restore_database(self, destination_host=None):
        """Loads previous database snapshot from disk."""
        fname = None
        if not settings.DEVICE_ID == self.server_device_id:
            raise TypeError('DB restore must be done from the server.')
        if self._get_db_engine() == 'mysql':
            fname = self._restore_mysql_database()
        if self._get_db_engine() == 'sqlite3':
            fname = self._restore_sqlite3_database()
        if not fname:
            raise RestoreError("Restore failed, unable to backup {0} database for {1}.".format(self._get_db_engine(), self.get_using_destination()))
        return fname
