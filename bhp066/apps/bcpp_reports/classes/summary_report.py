from django.db.models import Count

from bhp066.apps.bcpp_household.models import Plot


class SummaryReport(object):

    context = {}

    def update_report_model(self, label, value, value_format):
        try:
            report_model = self.report_model.objects.get(label=label)
            report_model.value = value
            report_model.value_format = value_format
        except self.report_model.DoesNotExist:
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
                        if not item['selected']:
                            plots_count = Plot.objects.filter(community=community, selected__isnull=True).count()
                            self.plots[community].update({'75_pct': plots_count})
                        elif item['selected'] == '1':
                            self.plots[community].update({'20_pct': item['selected__count']})
                        elif item['selected'] == '2':
                            self.plots[community].update({'05_pct': item['selected__count']})
                        else:
                            self.plots[community].update({item['selected']: item['selected__count']})
