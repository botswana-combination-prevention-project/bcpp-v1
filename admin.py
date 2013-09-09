from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location


class PrincipalInvestigatorAdmin(BaseModelAdmin):
    pass
admin.site.register(PrincipalInvestigator, PrincipalInvestigatorAdmin)


class  SiteLeaderAdmin(BaseModelAdmin):
    pass
admin.site.register(SiteLeader, SiteLeaderAdmin)


class  ProtocolAdmin(BaseModelAdmin):
    list_display = ('protocol_identifier', 'research_title')
admin.site.register(Protocol, ProtocolAdmin)


class  FundingSourceAdmin(BaseModelAdmin):
    pass
admin.site.register(FundingSource, FundingSourceAdmin)


class  SiteAdmin(BaseModelAdmin):
    list_display = ('site_identifier', 'location',)
admin.site.register(Site, SiteAdmin)


class  LocationAdmin(BaseModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)
