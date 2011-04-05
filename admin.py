from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource

class PrincipalInvestigatorAdmin(MyModelAdmin):
    pass  
admin.site.register(PrincipalInvestigator, PrincipalInvestigatorAdmin)


class  SiteLeaderAdmin(MyModelAdmin):
    pass  
admin.site.register( SiteLeader,  SiteLeaderAdmin)

class  ProtocolAdmin(MyModelAdmin):
    pass  
admin.site.register( Protocol,  ProtocolAdmin)

class  FundingSourceAdmin(MyModelAdmin):
    pass  
admin.site.register( FundingSource,  FundingSourceAdmin)

