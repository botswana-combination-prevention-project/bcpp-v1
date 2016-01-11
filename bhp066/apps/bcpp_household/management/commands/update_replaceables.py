# from django.core.management.base import BaseCommand, CommandError
# from bhp066.config.celery import already_running, CeleryTaskAlreadyRunning, CeleryNotRunning
#
# from bhp066.apps.bcpp_household.utils import update_replaceables
#
#
# class Command(BaseCommand):
#
#     help = 'List the online and replaceable status of a producer'
#
#     def handle(self, *args, **options):
#         try:
#             already_running(update_replaceables)
#             result = update_replaceables.delay()
#             print(('Task has been sent to the queue. Result: {0.result!r} ID: {0.id})'
#                    ).format(result))
#         except CeleryTaskAlreadyRunning as e_message:
#             raise CommandError(str(e_message))
#         except CeleryNotRunning as e_message:
#             raise CommandError(str(e_message))
#         except Exception as e_message:
#             raise CommandError('Unable to run task. Celery got {}.'.format(str(e_message)))
