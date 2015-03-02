import socket

from .celery import app as celery_app
from .exceptions import CeleryTaskAlreadyRunning, CeleryNotRunning


def already_running(celery_task):
    i = celery_app.control.inspect()
    try:
        activities = i.active().get('celery@{}'.format(socket.gethostname())) or {}
        for activity in activities:
            if celery_task.name in activity.get('name', []):
                raise CeleryTaskAlreadyRunning((
                    'Unable to start task. Task {} is already running ({} on {})'
                    ).format(celery_task.name, activity.get('id'), activity.get('hostname'),))
    except AttributeError:
        raise CeleryNotRunning(
            'Unable to inspect {}. Is celery running?'.format('celery@{}'.format(socket.gethostname())))
        pass
