from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import get_model
#from django.core.exceptions import ObjectDoesNotExist
#from django.http import Http404
from django import forms
from django.contrib.admin import widgets
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_birt_reports.models import ReportParameter
from bhp_birt_reports.models import BaseReport
from bhp_birt_reports.forms import ReportForm
from bhp_birt_reports.forms import ParametersForm

@login_required
def report_parameters(request, **kwargs):
    """ Gatheres the required parameters for a report"""
    reports = request.REQUEST['reports'].split(',')

    if reports and len(reports) > 1:
        raise TypeError('Please select only one report at a time.')
    if reports and len(reports) == 1:
        if not BaseReport.objects.filter(report_name=reports[0]).exists():
            raise TypeError('Report: {0}, does not exist in the system'.format(reports[0]))
    else:
        raise TypeError('No report chosen')
    report_params = ReportParameter.objects.filter(report__report_name=reports[0])
    fields = {}
    query_string = None
    for param in report_params:
        if param.is_active:
            if param.is_selectfield:
                #need to do this because we don't know which model we'd need to import
                #at runtime for the ModelChoiceField queryset.
                Model = get_model(param.app_name, param.model_name) 
                #Model = get_model('mochudi_household', 'household')
                query_string = param.query_string
                #evaluated = eval(query_string)
                #ModelMultipleChoiceField
                fields.update({param.parameter_name: forms.ModelMultipleChoiceField(label=param.parameter_name,queryset=eval(query_string),required=True,initial='DEFAULT')})
            else:
                if param.parameter_type == 'datetimefield':
                    fields.update({param.parameter_name: forms.DateTimeField(label=param.parameter_name,widget=widgets.AdminDateWidget)})
                    #fields[param.parameter_name].widget = fields[param.parameter_name].hidden_widget()
                elif param.parameter_type == 'charfield':
                    fields.update({param.parameter_name: forms.CharField(max_length=50, label=param.parameter_name,widget=forms.TextInput)})
                elif param.parameter_type == 'integerfield':
                    fields.update({param.parameter_name: forms.IntegerField(label=param.parameter_name,widget=forms.TextInput)})
                elif param.parameter_type == 'doublefield':
                    fields.update({param.parameter_name: forms.DecimalField(label=param.parameter_name,widget=forms.TextInput)})
    form = type('ContactForm', tuple([forms.BaseForm]), { 'base_fields': fields })
    return render_to_response(
        #'entere_parameters.html', {'params': report_params, 'report': reports[0]},
        'entere_parameters_form.html', {'params': report_params, 'report': reports[0], 'form': form},
        context_instance=RequestContext(request)
        )
