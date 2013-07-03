import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
#from bhp_crypto.classes import Cryptor
from bhp_birt_reports.classes import ReportDecryptor

@login_required
def generate_report(request, **kwargs):
    """ Return items from the producer to the source."""
    data = request.POST
    report_name = None
    token_string = '\"'
    flag = False
    run_string = 'java -jar'+' '+settings.REPORTS_JAR_PATH+' '+settings.REPORTS_TEMPLATES_PATH+' '+settings.REPORTS_OUTPUT_PATH+' '+request.user.username
    for key, value in data.iteritems():
        if key == 'report':
            report_name = value
            continue 
        if key != 'csrfmiddlewaretoken':
            tokens = value.split(' ')
            if len(tokens) > 1:
                for tk in tokens:
                    token_string = token_string + tk + ' '
                token_string = token_string.rstrip()
                token_string = token_string+'\"'
                flag = True
            if flag:
                value = token_string
                flag = False
            run_string = run_string +' '+key+' '+value
    run_string +=' '+report_name
    #print run_string
    result = os.system(run_string)
    #java -jar ~/Documents/birtreport_generator.jar structures_yr_2 STARTING_DATE 2013-05-01 csrfmiddlewaretoken yRyoq2DbHHRlcpmWT7AedhOQZs33sUxS SECTION Section A WARD Ntshinoge
    if result != 0:
        raise TypeError('java jar file did not complete successfully')
    f = open(settings.REPORTS_OUTPUT_PATH+'report_'+request.user.username+'_'+report_name+'.html')
    lines = f.readlines()
    f.close()
    count = 0
    for line in lines:
        if line.find('enc1:::') != -1:
            print line
            lines[count] = ReportDecryptor().decrypt(line)
        count+=1
    f = open(settings.REPORTS_OUTPUT_PATH+'report_'+request.user.username+'_'+report_name+'.html','w')
    for line in lines:
        f.write(line+'\n')
    f.close()
    return render_to_response(
        'report_'+request.user.username+'_'+report_name+'.html', {},
        context_instance=RequestContext(request)
        )
