from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'bcpp_household/', include('bcpp_household.urls')),
    url(r'bcpp_household_member/', include('bcpp_household_member.urls')),
    url(r'bcpp_subject/', include('bcpp_subject.urls')),
    url(r'bcpp_lab/', include('bcpp_lab.urls')),
    url(r'bcpp_survey/', include('bcpp_survey.urls')),
]
