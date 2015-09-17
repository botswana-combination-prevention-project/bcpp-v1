from django import forms

from ..models import SubjectRequisitionInspector


class RequisitionInspectorForm (forms.Form):

    class Meta:
        model = SubjectRequisitionInspector
