from django.db import connection


class LockableObject(object):

    """
        http://djangosnippets.org/snippets/2443/
    """

    default_timeout = 45

    def __init__(self, *args, **kwargs):

        super(LockableObject, self).__init__(*args, **kwargs)

        self.dbcursor = connection.cursor()
        self.lock_id = None

    def get_lock_name(self):
        return '%s|%s' % (self.__class__.__name__,
                          self.lock_id)

    def lock(self):

        if hasattr(self, 'id'):
            self.lock_id = self.id
        else:
            self.lock_id = 0

        lock_name = self.get_lock_name()

        self.dbcursor.execute('select get_lock("%s",%s) as lock_success' % (lock_name,
                                                                            self.default_timeout))

        success = (self.dbcursor.fetchone()[0] == 1)

        if not success:
            raise EnvironmentError, 'Acquiring lock "%s" timed out after %d seconds' % (lock_name, self.default_timeout)

        return success

    def unlock(self):
        self.dbcursor.execute('select release_lock("%s")' % self.get_lock_name())


def require_object_lock(func):

    def wrapped(*args, **kwargs):

        lock_object = args[0]

        lock_object.lock()

        try:
            return func(*args, **kwargs)
        finally:
            lock_object.unlock()

    return wrapped


"""
##########################################################################
# Example

from django.db import models
from django.core.mail import mail_admins

class Notification(models.Model, LockableObject):
    message = models.CharField()
    sent = models.BooleanField()

    @require_object_lock
    def send(self):
        if not self.sent:
            mail_admins('Notification',
                        self.message)
            self.sent = True
            self.save()

a = Notification(message='Hello world',
                 sent=False)

# Important to save; we can't lock a specific object without it having
# an 'id' attribute.
a.save()

a.send()

# Now, we are guaranteed that no matter how many threads try, and no
# matter their timing, calls to the send() method of this row's object
# can only generate ONE mail_admins() call.  We've prevented the race
# condition of two threads calling send() at the same time and both of
# them seeing self.sent as False and sending the mail twice.
#
# Note that if mail_admins failed and threw an exception, the
# require_object_lock decorator catches the exception, releases the
# lock, then raises it to let it fulfill its normal behavior.

"""
