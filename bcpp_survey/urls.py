from django.conf.urls import url

from .admin_site import bcpp_survey_admin

urlpatterns = [
    url(r'^admin/', bcpp_survey_admin.urls),
]
