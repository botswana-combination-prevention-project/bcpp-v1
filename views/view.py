# Create your views here.
"""
import pyodbc
from bhp_lab_temptables.models import LabSimpleResult
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from bhp_lab_result_report.lab_specimens import fetch_receiving

def detail(request, report_id):
	p = get_object_or_404(LabSimpleResult, pk=report_id)
	return render_to_response('detail.html', {'obj': p})

def view(request, report_id):
	p = get_object_or_404(LabSimpleResult, pk=report_id)
	result = fetch_receiving(p.sample_id)
    
	return render_to_response('view.html', {'obj': result})
	
def printPDF(request, report_id):
	return HttpResponse("You're printing result %s." % report_id)
"""
