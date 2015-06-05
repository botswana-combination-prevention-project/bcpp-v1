from django import forms
from django.forms.util import ErrorList
from datetime import datetime, timedelta

from edc.base.form.forms import BaseModelForm

from ..models import Tracker, SiteTracker

from ..constants import INACCESSIBLE, CONFIRMED, ACCESSIBLE


class TrackerForm(BaseModelForm):

    class Meta:
        model = Tracker


class SiteTrackerForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(SiteTrackerForm, self).clean()
        return cleaned_data

    class Meta:
        model = SiteTracker
