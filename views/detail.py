# Create your views here.
import pyodbc
from reports.models import Labtemp
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from utils.lab_specimens import fetch_receiving

def detail(request, report_id):
	p = get_object_or_404(Labtemp, pk=report_id)
	return render_to_response('reports/detail.html', {'obj': p})

def view(request, report_id):
	p = get_object_or_404(Labtemp, pk=report_id)
	result = fetch_receiving(p.sample_id)
    
	return render_to_response('reports/view.html', {'obj': result})
	
def printPDF(request, report_id):
	return HttpResponse("You're printing result %s." % report_id)
