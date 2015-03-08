from edc.map.classes import site_mappers

from ..helpers import Community

from .base_collector import BaseCollector


class Communities(BaseCollector):
    """Exports helper.community instances to CSV.

    For example::
        from apps.bcpp_export.collectors import Communities

        communities = Communities()
        communities.export_to_csv()
    """

    def __init__(self, export_plan=None, community=None, exception_cls=None):
        super(Communities, self).__init__(export_plan=export_plan, community=community, exception_cls=exception_cls)
        site_mappers.autodiscover()
        try:
            del site_mappers._registry['bhp']
        except KeyError:
            pass
        try:
            del site_mappers._registry['test_community']
        except KeyError:
            pass
        if community:
            self.mappers = [site_mappers.get(community)]
        else:
            self.mappers = [mapper for mapper in site_mappers]

    def export_to_csv(self):
        for mapper in self.mappers:
            community = Community(mapper)
            self._export(community)
