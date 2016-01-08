import csv
import os
import pprint
from datetime import datetime

from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.choices import (NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE, RESIDENTIAL_HABITABLE)
from bhp066.apps.bcpp_household.helpers.replacement_helper import ReplacementHelper
from bhp066.apps.bcpp_household.models import Plot, HouseholdStructure, HouseholdLogEntry

from ...choices import INACCESSIBLE


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse> <survey_slug e.g bcpp_year_one>'
    help = 'Creates a csv file of plots from the 25% (selected=1/2) to be added to the HTC campaign (CDC).'

    def handle(self, *args, **options):
        """Writes to csv plot information for export to CDC.

        The exported data is a selection of plots from the original 25% that
        are to be added to the HTC campaign."""
        try:
            community_name = args[0]
            survey = Survey.objects.get(survey_slug=args[1])
        except IndexError:
            args = args or ['None']
            raise CommandError('Expected two arguments. Got {}'.format(' '.join(args)))
        except Survey.DoesNotExist:
            raise CommandError('Unknown survey slug. Expected one of {}. Got {}'.format(
                ', '.join([x.survey_slug for x in Survey.objects.all()]), args[1]))

        plots = Plot.objects.filter(community=community_name).exclude(Q(bhs=True) | Q(htc=True))
        if not plots.count() == Plot.objects.filter(
                community=community_name, selected__isnull=False).exclude(Q(bhs=True) | Q(htc=True)).count():
            raise CommandError((
                'Expected all plots not flagged as BHS or HTC to be from the pool of 25%. Got {} != {}').format(
                    plots.count(),
                    Plot.objects.filter(
                        community=community_name, selected__isnull=False).exclude(Q(bhs=True) | Q(htc=True)).count()))
        print 'HTC: {} ({}, {}, {})'.format(
            Plot.objects.filter(community=community_name, htc=True).count(),
            Plot.objects.filter(community=community_name, htc=True, selected__isnull=True).count(),
            Plot.objects.filter(community=community_name, htc=True, selected=1).count(),
            Plot.objects.filter(community=community_name, htc=True, selected=2).count())
        print 'BHS: {} ({}, {}, {})'.format(
            Plot.objects.filter(community=community_name, bhs=True).count(),
            Plot.objects.filter(community=community_name, bhs=True, selected__isnull=True).count(),
            Plot.objects.filter(community=community_name, bhs=True, selected=1).count(),
            Plot.objects.filter(community=community_name, bhs=True, selected=2).count())

        print 'Unallocated from 25%: {}'.format(plots.count())
        header_row = ['plot_identifier', 'action', 'status', 'household_count',
                      'gps_target_lat', 'gps_target_lon', 'enrolled', 'comment']
        target_path = '~/plot_list_{}_25_pct_update_{}.csv'.format(
            community_name, datetime.today().strftime('%Y%m%d%H%M'))
        cnt = 0
        status_options = {}
        with open(os.path.expanduser(target_path), 'w') as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow(header_row)
            # determine a status comment on each plot
            for plot in Plot.objects.filter(
                    community=community_name,
                    selected__isnull=False).exclude(bhs=True).order_by('selected', 'plot_identifier'):
                status = []
                if plot.bhs:
                    # enrolled in bhs
                    status = ['bhs'.format(plot.selected)]
                elif plot.htc:
                    # flagged by BHS to hand over to htc on replacement
                    if plot.status in [NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]:
                        status = ['--- {}'.format(plot.status, plot.selected or '0')]
                    else:
                        status = ['htc'.format(plot.selected or '0')]
                else:
                    if plot.status is None:
                        # plot never confirmed or replaced, give to htc
                        status.append('htc {}'.format(plot.action, plot.selected))
                    elif plot.status in [INACCESSIBLE, NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE]:
                        # not a plot
                        status.append('--- {}'.format(plot.status, plot.selected))
                    elif plot.status == RESIDENTIAL_HABITABLE:
                        if plot.household_count == 0:
                            raise TypeError('Unexpected plot status, household_count==0')
                        else:
                            for household_structure in HouseholdStructure.objects.filter(
                                    survey=survey, household__plot=plot).exclude(enrolled=True):
                                if HouseholdLogEntry.objects.filter(
                                        household_log__household_structure=household_structure):
                                    household_structure.household.replaced_by = None
                                    replacement_helper = ReplacementHelper(household_structure=household_structure)
                                    if not replacement_helper.household_replacement_reason:
                                        replacement_reason = ''.join(
                                            [log.household_status for log in HouseholdLogEntry.objects.filter(
                                                household_log__household_structure=household_structure).order_by(
                                                    'created')][-1:]) or '-'
                                        if replacement_reason == 'eligible_representative_present':
                                            replacement_reason = 'eligible_representative_present-no_bhs_eligibles'
                                    status.append(
                                        'htc {}'.format(
                                            (replacement_helper.household_replacement_reason or replacement_reason
                                             ).replace(' ', '_'))
                                    )
                    else:
                        raise TypeError('Unexpected plot status')
                if status:
                    status = '{}'.format(', '.join(status))
                else:
                    status = 'htc not visited'
                print status
                cnt += 1
                writer.writerow([plot.plot_identifier, plot.action, plot.status, plot.household_count,
                                 plot.gps_target_lat, plot.gps_target_lon, 'Yes' if plot.bhs else 'No',
                                 status])
                for s in status.split(','):
                    try:
                        status_options[s] += 1
                    except KeyError:
                        status_options.update({s: 1})
        print 'exported {} records of {}.'.format(cnt, Plot.objects.filter(
            community=community_name, selected__isnull=False).order_by('selected', 'plot_identifier').count())
        print os.path.expanduser(target_path)
        pprint.pprint(status_options, indent=2)
