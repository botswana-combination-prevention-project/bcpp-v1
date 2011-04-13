# Create your views here.
import pyodbc
from bhp_lab_result.models import Labtemp
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from bhp_lab_result_report.lab_specimens import fetch_receiving

def index(request):
	cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
	cursor = cnxn.cursor()
	cursor.execute("select top 100 * from mochudi_labtemp")
	Labtemp.objects.all().delete()
	
	for row in cursor:
		obj = Labtemp(
		subject_identifier=row.subject_identifier,
		initials=row.initials,
		dob=row.dob,
		sample_id=row.sample_id,
		date_sample_drawn=row.date_sample_drawn,
		test=row.test,
		received=row.received,
		created=row.created,
		modified=row.modified,
		user_created=row.user_created,
		user_modified=row.user_modified,
		utestid=row.utestid,
		result=row.result,
		result_quantifier=row.result_quantifier,
		import_date=row.import_date)
		
		obj.save() 
	
	cursor.close() 
	latest_results_list = Labtemp.objects.all().order_by('-import_date')[:30]
	return render_to_response('reports/index.html', {'latest_results_list': latest_results_list})

	#return HttpResponse("Hello, world. You're at the results index.")



