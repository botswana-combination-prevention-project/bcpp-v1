from django import forms
from bcpp_inspector.models import SubjectRequisitionInspector


class RequisitionInspectorForm (forms.Form):

    class Meta:
        model = SubjectRequisitionInspector
