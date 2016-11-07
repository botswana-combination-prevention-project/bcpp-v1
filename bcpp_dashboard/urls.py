from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .classes import SubjectDashboard, HouseholdDashboard, ClinicDashboard
from .views import ParticipationView

urlpatterns = []

for pattern in HouseholdDashboard.get_urlpatterns():
    urlpatterns.append(
        url(pattern,
            login_required(HouseholdDashboard.as_view()),
            name=HouseholdDashboard.dashboard_url_name)
    )

for pattern in SubjectDashboard.get_urlpatterns():
    urlpatterns.append(
        url(pattern,
            login_required(SubjectDashboard.as_view()),
            name=SubjectDashboard.dashboard_url_name)
    )

for pattern in ClinicDashboard.get_urlpatterns():
    urlpatterns.append(
        url(pattern,
            login_required(ClinicDashboard.as_view()),
            name=ClinicDashboard.dashboard_url_name)
    )

urlpatterns.append(
    url(r'participation/',
        login_required(ParticipationView.as_view()),
        name='participation_url')
)
