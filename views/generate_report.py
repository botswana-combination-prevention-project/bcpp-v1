import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_birt_reports.classes import ReportDecryptor

@login_required
def generate_report(request, **kwargs):
    """ Return items from the producer to the source."""
    data = request.POST
    report_name = None
    token_string = '\"'
    flag = False
    vital_contants = ['REPORTS_JAR_PATH','REPORTS_TEMPLATES_PATH','REPORTS_OUTPUT_PATH']
    for cons in vital_contants:
        if cons not in dir(settings):
            raise TypeError('Please add \'{0}\' to the settings file'.format(cons))
    run_string = 'java -jar'+' '+settings.REPORTS_JAR_PATH+' '+settings.REPORTS_TEMPLATES_PATH+' '+settings.REPORTS_OUTPUT_PATH+' '+request.user.username
    for key in data.keys():
        if key == 'report':
            report_name = data[key]
            continue 
        if key != 'csrfmiddlewaretoken':
            values_list = data.getlist(key,None)
            run_string = run_string +' '+key +' '+ str(len(values_list))
            if values_list:
                for value_item in values_list:
                    tokens = value_item.split(' ')
                    if len(tokens) > 1:
                        for tk in tokens:
                            token_string = token_string + tk + ' '
                        token_string = token_string.rstrip()
                        token_string = token_string+'\"'
                        flag = True
                    if flag:
                        value_item = token_string
                        flag = False
                        token_string = '\"'
                    run_string = run_string +' '+ value_item
#     for key, value in data.iteritems():
#         print key
#         print data.getlist(key,'NONE')
# #         print data
# #         print key
# #         print data[key]
# #         print value
#         if key == 'report':
#             report_name = value
#             continue 
#         if key != 'csrfmiddlewaretoken':
#             tokens = value.split(' ')
#             if len(tokens) > 1:
#                 for tk in tokens:
#                     token_string = token_string + tk + ' '
#                 token_string = token_string.rstrip()
#                 token_string = token_string+'\"'
#                 flag = True
#             if flag:
#                 value = token_string
#                 flag = False
#             run_string = run_string +' '+key+' '+value
    run_string +=' '+report_name
    #print run_string
    result = os.system(run_string)
    #java -jar ~/Documents/birtreport_generator.jar /Users/sirone/Documents/workspace/bhp041_survey/ /Users/sirone/Documents/workspace/bhp041_survey/bhp_birt_reports/templates/ onep TOWN 1 LOBATSE WARD_SECTION 3 "Sections A" "Sections B" "Sections C" INVESTIGATOR 1 ONEP targeted_by_section
    if result != 0:
        raise TypeError('java jar file did not complete successfully')
    f = open(settings.REPORTS_OUTPUT_PATH+'report_'+request.user.username+'_'+report_name+'.html')
    lines = f.readlines()
    f.close()
    count = 0
    for line in lines:
        if line.find('enc1:::') != -1:
            lines[count] = ReportDecryptor().decrypt(line)
        count+=1
    f = open(settings.REPORTS_OUTPUT_PATH+'report_'+request.user.username+'_'+report_name+'.html','w')
    for line in lines:
        f.write(line+'\n')
    f.close()
    report = 'report_'+request.user.username+'_'+report_name+'.html'
    return render_to_response(
        #'report_'+request.user.username+'_'+report_name+'.html', {},
        'render_report_template.html', {'report' : report},
        context_instance=RequestContext(request)
        )
