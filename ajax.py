from django.template.loader import render_to_string
from dajax.core import Dajax
from django.db.models import get_model
from dajaxice.decorators import dajaxice_register
from lab_clinic_api.classes import EdcLab, ResultContext


@dajaxice_register
def plot_longitudinal_results(request, subject_identifier, test_code):
    dajax = Dajax()
    rendered = render_to_string('plot_result.html', {'subject_identifier': subject_identifier, 'test_code': test_code})
    dajax.assign('#left_table', 'innerHTML', rendered)
    return dajax.json()


@dajaxice_register
def updating(request):
    dajax = Dajax()
    dajax.assign('#x_results', 'innerHTML', 'Contacting lab,<BR>please wait...(may take 1 to 2 mins)<BR>')
    return dajax.json()


@dajaxice_register
def update_result_status(request, subject_identifier, output=True):
    dajax = Dajax()
    if subject_identifier:
        edc_lab = EdcLab()
        rendered = edc_lab.render(subject_identifier, True)
        dajax.assign('#x_results', 'innerHTML', rendered)
    if not output:
        return None
    return dajax.json()


@dajaxice_register
def view_result_report(request, result_identifier):
    dajax = Dajax()
    Result = get_model('lab_clinic_api', 'result')
    ResultItem = get_model('lab_clinic_api', 'resultitem')
    result = Result.objects.filter(result_identifier=result_identifier)
    result_items = ResultItem.objects.filter(result=result)
    result_context = ResultContext(result, result_items)
    rendered = render_to_string('clinic_result_report.html', result_context.context)
    dajax.assign('#left_table', 'innerHTML', rendered)
    return dajax.json()


@dajaxice_register
def view_receive_ajax(request, receive_identifier):
    #print receive_identifier
    dajax = Dajax()
    lab_context = LabContext(receive_identifier=receive_identifier)
    rendered = render_to_string('clinic_result_report.html', lab_context.context)
    dajax.assign('#left_table', 'innerHTML', rendered)
    return dajax.json()
