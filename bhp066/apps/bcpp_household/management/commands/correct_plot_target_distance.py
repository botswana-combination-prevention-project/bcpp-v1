from optparse import make_option

from django.db.models import get_model
from django.core.management.base import BaseCommand, CommandError

from edc.map.classes import site_mappers

from ...constants import CONFIRMED


class Command(BaseCommand):
    """ Corrects the target radius in plot enrolled with radius > 25m but without an IncreasePlotRadius record
    """
    args = '--community <community>, --fix <True|False>'

    help = ('Corrects the target radius in plot enrolled with radius > 25m but without an IncreasePlotRadius record'
            ' for plots of community x. Specify --fix (True|False) to fix or do a dry run')

    option_list = BaseCommand.option_list + (
        make_option(
            '--community',
            dest='community',
            action='store_true',
            default=False,
            help=('Enter community')),
        make_option(
            '--fix',
            dest='fix',
            action='store_true',
            default=False,
            help=('Fix or dry run')),
    )

    def handle(self, *args, **options):
        if len(args) == 2:
            pass
        else:
            raise CommandError('Command expecting Two arguments, being --community <community>, --fix <True|False>')
        if options['community'] and options['community']:
            self.correct_target_distance(args[0], args[1])
        else:
            raise CommandError('Command expecting Two arguments, being --community <community>, --fix <True|False>')

    def correct_target_distance(self, community, fix):
        to_fix = []
        Plot = get_model('bcpp_household', 'Plot')
        IncreasePlotRadius = get_model('bcpp_household', 'IncreasePlotRadius')
        print "======================================="
        print ".....Correcting for community={}".format(community)
        plots = Plot.objects.filter(community=community, action=CONFIRMED).exclude(htc=True)
        print ".....Found {} confirmed Plots for community {}".format(plots.count(), community.upper())
        for plot in plots:
            if plot.distance_from_target > (0.025 * 1000) and not IncreasePlotRadius.objects.filter(plot=plot).exists():
                to_fix.append(plot)
        print (".....Found {} Plots for community {} which are confirmed at radius > 25m, but with no"
               " IncreasePlotRadius record").format(len(to_fix), community.upper())
        if fix.lower() != 'true':
            print ".....This was a dry run use --fix True in order to persist the correction"
        elif fix.lower() == 'true':
            count = 0
            for plt in to_fix:
                count += 1
                IncreasePlotRadius.objects.create(plot=plt, radius=plt.distance_from_target)
                try:
                    plot_radius = IncreasePlotRadius.objects.get(plot=plt)
                    plot_radius.save()
                    print ".....SUCCESS: {}/{} Plot {}".format(count, len(to_fix), plt.plot_identifier)
                except IncreasePlotRadius.DoesNotExist:
                    print ".....IncreasePlotRadius.DoesNotExist: {}/{} Plot {}".format(
                        count, len(to_fix), plt.plot_identifier)
        else:
            pass
