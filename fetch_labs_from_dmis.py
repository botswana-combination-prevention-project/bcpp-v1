import pyodbc
from reports.models import Labtemp


def fetch_labs_from_dmis():

	cnxn = pyodbc.connect("DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;DATABASE=BHPLAB")
	cursor = cnxn.cursor()

	#cursor.execute("drop table mochudi_labtemp")
	#cursor.execute("select *, getdate() as import_date into mochudi_labtemp from (select l.pat_id as subject_identifier, l.pinitials as initials, convert(varchar, dob, 121) as dob, l.pid as sample_id, convert(varchar, l.sample_date_drawn, 121) as date_sample_drawn, l.tid as test, convert(varchar, l.headerdate, 121) as received, convert(varchar,l.datecreated, 121) as created, convert(varchar,l.datelastmodified, 121) as modified, l.keyopcreated as user_created, l.keyoplastmodified as user_modified, utestid, result, result_quantifier from LAB01Response as l left join lab21Response as l21 on l21.pid=l.pid left join lab21ResponseQ001X0 as l21d on l21.q001x0=l21d.qid1x0 where sample_protocolnumber='BHP041' and l21d.status='F'
	
	 UNION select l.pat_id as subject_identifier, l.pinitials as initials, convert(varchar, dob, 121) as dob, l.pid as sample_id, convert(varchar, l.sample_date_drawn, 121) as date_sample_drawn, l.tid as test, convert(varchar, l.headerdate, 121) as received, convert(varchar,l.datecreated, 121) as created, convert(varchar,l.datelastmodified, 121) as modified, l.keyopcreated as user_created, l.keyoplastmodified as user_modified, utestid, result, result_quantifier from LAB01Response as l left join lab21Response as l21 on l21.pid=l.pid left join lab21ResponseQ001X0 as l21d on l21.q001x0=l21d.qid1x0 where l21d.id is null and sample_protocolnumber='BHP041') as A")

	cursor.execute("select top 100 * from mochudi_labtemp")
#	for row in cursor:
#		print 'subject_identifier=%s initials=%s,' % (row.subject_identifier,row.initials)

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

	try:
		cursor.close()          
	except:
		pass
        
	return Labtemp.objects.all().count()        

   
    


