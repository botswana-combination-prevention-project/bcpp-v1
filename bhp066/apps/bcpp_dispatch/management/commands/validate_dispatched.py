from optparse import make_option

from django.core.management.base import BaseCommand

from edc.device.dispatch.models import DispatchItemRegister

from bhp066.apps.bcpp_household.models import Plot, Household


class Command(BaseCommand):
    """ Sends an email to a list of recipients about the status of uploading transaction files
    """
    args = ('--all_twenty', '--all_replacing')

    help = 'Reconcile dispatch item registers with the producer.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--all_twenty',
            dest='all_twenty',
            action='store_true',
            default=False,
            help=('Check all plots in 20% are dispatched')),
        make_option(
            '--all_replacing',
            dest='all_replacing',
            action='store_true',
            default=False,
            help=('Check all plots marked as replacing other plots are dispatched')),
    )

    def handle(self, *args, **options):
        if options['all_twenty']:
            self.all_20pcnt_dispatched()
        elif options['all_replacing']:
            self.all_replacing_dispatched()
        else:
            pass

    def all_20pcnt_dispatched(self):
        twenty_pcnt = Plot.objects.filter(selected=1)
        count = 0
        print '================================='
        for plt in twenty_pcnt:
            try:
                DispatchItemRegister.objects.get(item_model_name='plot', item_pk=plt.id)
            except DispatchItemRegister.DoesNotExist:
                count += 1
                print 'Plot identifier={}, in 20% is NOT DISPATCHED'.format(plt.plot_identifier)
        print 'Total in 20%={}, Total Not Dispatched={}'.format(twenty_pcnt.count(), count)
        print 'DONE'
        print '================================='

    def all_replacing_dispatched(self):
        five_pcnt = Plot.objects.filter(selected=2)
        count = 0
        print '================================='
        for plt in five_pcnt:
            if plt.replaces:
                try:
                    DispatchItemRegister.objects.get(item_model_name='plot', item_pk=plt.id)
                except DispatchItemRegister.DoesNotExist:
                    count += 1
                    try:
                        replaced = Plot.objects.get(plot_identifier=plt.replaces)
                    except Plot.DoesNotExist:
                        replaced = Household.objects.get(household_identifier=plt.replaces)
                    if replaced._meta.module_name == 'household':
                        replaced = replaced.plot
                    else:
                        replaced = replaced
                    replaced_item = DispatchItemRegister.objects.get(item_pk=replaced.id)
                    print ('Plot identifier={}, in 5% which Replaces \'{}\' is NOT DISPATCHED. {} '
                           'is in producer {}').format(
                               plt.plot_identifier,
                               plt.replaces,
                               plt.plot_identifier,
                               replaced_item.producer.name)
        print 'Total in 5%={}, Total Replacing Not Dispatched={}'.format(five_pcnt.count(), count)
        print 'DONE'
        print '================================='
