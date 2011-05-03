from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_research_protocol.models import Protocol, PrincipalInvestigator, SiteLeader, FundingSource, Site, ResearchClinic, Location

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

class  SiteAdmin(MyModelAdmin):
    pass  
admin.site.register( Site,  SiteAdmin)

class  ResearchClinicAdmin(MyModelAdmin):
    pass  
admin.site.register( ResearchClinic,  ResearchClinicAdmin)

class  LocationAdmin(MyModelAdmin):
    pass  
admin.site.register( Location,  LocationAdmin)

