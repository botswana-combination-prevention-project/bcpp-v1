from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, Location

class PrincipalInvestigatorAdmin(MyModelAdmin):
    pass  
admin.site.register(PrincipalInvestigator, PrincipalInvestigatorAdmin)

class  SiteLeaderAdmin(MyModelAdmin):
    pass  
admin.site.register( SiteLeader,  SiteLeaderAdmin)

class  ProtocolAdmin(MyModelAdmin):
    list_display = ('protocol_identifier', 'research_title')  
admin.site.register( Protocol,  ProtocolAdmin)

class  FundingSourceAdmin(MyModelAdmin):
    pass  
admin.site.register( FundingSource,  FundingSourceAdmin)

class  SiteAdmin(MyModelAdmin):
    list_display = ('site_identifier', 'location', )
admin.site.register( Site,  SiteAdmin)

class  LocationAdmin(MyModelAdmin):
    pass  
admin.site.register( Location,  LocationAdmin)

