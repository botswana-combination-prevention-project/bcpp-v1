
from django import forms

from edc.base.form.forms import BaseModelForm

from ..models import NotebookPlotList


class NotebookPlotListForm(forms.ModelForm):

    pass

    class Meta:
        model = NotebookPlotList
