import logging
from django.core.management.base import BaseCommand
from django.db.models import signals

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Command(BaseCommand):

    args = ''
    help = 'list signals for this project'

    def handle(self, *args, **options):
        print 'pre_save signals:'
        pre_save = [r[0][0] for r in signals.pre_save.receivers]
        if pre_save:
            pre_save = list(set(pre_save))
            pre_save.sort()
            print '  {0}\n  {1}'.format(pre_save[0], '\n  '.join(pre_save[1:]))
        print 'post_save signals:'
        post_save = [r[0][0] for r in signals.post_save.receivers]
        if post_save:
            post_save = list(set(post_save))
            post_save.sort()
            print '  {0}\n  {1}'.format(post_save[0], '\n  '.join(post_save[1:]))
        print 'post_delete signals:'
        post_delete = [r[0][0] for r in signals.post_delete.receivers]
        if post_delete:
            post_delete = list(set(post_delete))
            post_delete.sort()
            print '  {0}\n  {1}'.format(post_delete[0], '\n  '.join(post_delete[1:]))
        print 'm2m_changed signals:'
        m2m_changed = [r[0][0] for r in signals.m2m_changed.receivers]
        if m2m_changed:
            m2m_changed = list(set(m2m_changed))
            m2m_changed.sort()
            print '  {0}\n  {1}'.format(m2m_changed[0], '\n  '.join(m2m_changed[1:]))
