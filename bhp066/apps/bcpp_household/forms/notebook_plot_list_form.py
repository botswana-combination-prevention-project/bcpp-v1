from django import forms

from ..models import NotebookPlotList


class NotebookPlotListForm(forms.ModelForm):

    pass

    class Meta:
        model = NotebookPlotList
