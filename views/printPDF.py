# Create your views here.
import pyodbc
from reports.models import Labtemp
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from utils.lab_specimens import fetch_receiving
	
def printPDF(request, report_id):
	return HttpResponse("You're printing result %s." % report_id)
