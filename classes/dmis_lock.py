from lab_import_dmis.models import DmisLock as DmisLockModel


class DmisLock(object):
    """ Locks out others from initiating a dmis import for the given protocol or subject. """

    def __init__(self, db):
        self.db = db
        self.lock = None
        self.is_locked = False

    def get_lock(self, lock_name):
        if not self.lock:
            try:
                self.lock = DmisLockModel.objects.using(self.db).create(lock_name=lock_name)
            except:
                self.lock = None
        return self.lock

    def release(self):
        try:
            self.lock.delete()
            self.lock = None
            self.is_locked = False
            return True
        except:
            return False

    def check(self):
        return self.is_locked
