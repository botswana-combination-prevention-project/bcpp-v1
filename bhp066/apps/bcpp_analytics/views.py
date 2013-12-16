from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#from apps.bcpp_subject.models.hiv_testing_history import HivTestingHistory
from apps.bcpp.choices import COMMUNITIES
from .report_queries.household_report_query import HouseholdReportQuery
from .report_queries.household_member_report_query import HouseholdMemberReportQuery
from .report_queries.plot_report_query import PlotReportQuery


@login_required
def index(request):
    template = "bcpp_analytics/analytics_index.html"
    return render(request, template, {})


@login_required
def accrual(request):
    template = "bcpp_analytics/accrual_report.html"
    communities = [item[0] for item in COMMUNITIES]
    community1 = request.GET.get("community1") or 'Ranaka'
    community2 = request.GET.get("community2") or 'Digawana'

    plots = (PlotReportQuery(community1), PlotReportQuery(community2))
    households = (HouseholdReportQuery(community1), HouseholdReportQuery(community2))
    members = (HouseholdMemberReportQuery(community1), HouseholdMemberReportQuery(community2))

    page_context = {'communities': communities,
                    'plots': plots,
                    'households': households,
                    'members': members,
                    }
    return render(request, template, page_context)
