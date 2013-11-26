from django.db.models import Count

from apps.bcpp_household.models import Plot, Household, HouseholdStructure

#from ..models import Report01


class SummaryReport(object):

#    report_model = Report01
    context = {}

    def update_report_model(self, label, value, value_format):
        try:
            report_model = self.report_model.objects.get(label=label)
            report_model.value = value
            report_model.value_format = value_format
        except:
            report_model = self.report_model.objects.create(label=label, value=value, value_format=value_format)

    def update(self, community=None):

        # total by community
        self.plots = {}
        plots = Plot.objects.values('community').annotate(Count('community'))
        communities = [plot['community'] for plot in plots]
        for item in Plot.objects.values('community').annotate(Count('community')):
            for community in communities:
                if item['community'] == community:
                    self.total_plots = Plot.objects.filter(community=community).count()
                    # total plots
                    self.plots[community] = {'Total': self.total_plots}
                    # total by selection category
                    for item in Plot.objects.filter(community=community).values('selected').annotate(Count('selected')):
                        if item['selected'] == None:
                            self.plots[community].update({'75_pct': Plot.objects.filter(community=community, selected__isnull=True).count()})
                        elif item['selected'] == '1':
                            self.plots[community].update({'20_pct': item['selected__count']})
                        elif item['selected'] == '2':
                            self.plots[community].update({'05_pct': item['selected__count']})
                        else:
                            self.plots[community].update({item['selected']: item['selected__count']})
#
#
#
#         for item in Plot.objects.values('selected', 'community', 'action', 'status').annotate(
#                 selection_category_cnt=Count('selected'),
#                 community_cnt=Count('community'),
#                 confirmed_cnt=Count('action'),
#                 status_cnt=Count('status')):
#             self.plots.update(item)
