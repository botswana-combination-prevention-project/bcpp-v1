from datetime import datetime, date, time, timedelta
from django.db.models import get_model
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from bhp_common.models import MyBasicModel
from bhp_model_selector.classes import ModelSelector
from audit_trail.forms import AuditTrailForm

@login_required
def audit_trail_view(request, **kwargs):

    """ Using app_label and model_name present the cls+'_audit' table"""
    
    section_name = kwargs.get('section_name')
    app_label = kwargs.get('app_label')
    model_name = kwargs.get('model_name')

    field_labels = []
    field_names = []
    display_rows = []    
    model = None
    history = None
    report_title = 'Audit Trail'
    app_label = ''
    model_name = ''
    verbose_name = ''
    template = 'audit_trail.html'     
    err_message = ''
    status_message = ''    
    audit_subject_identifier = None    


    if request.method == 'POST':
        
        # form to select the app and model
        form = AuditTrailForm(request.POST)                        

        if form.is_valid():

            app_label = form.cleaned_data['app_label']
            model_name = form.cleaned_data['model_name']
            audit_subject_identifier = form.cleaned_data['audit_subject_identifier']                
            dashboard_type = form.cleaned_data['dashboard_type']
            visit_code = form.cleaned_data['visit_code']
            visit_instance = form.cleaned_data['visit_instance']
            back_url_name = form.cleaned_data['back_url_name']            
            

            model_selector = ModelSelector(app_label, model_name)             
            
            if app_label and model_name:
                try:
                    # try to get the model and access the history manager, or fail.
                    model = get_model(app_label, model_name)
                    history = model.history.all().order_by('_audit_id')
                    verbose_name = model._meta.verbose_name
                    report_title  = 'Audit Trail for {app_label}.{model_name}'.format(app_label=app_label, model_name=model._meta.verbose_name)
                except:
                    err_message = 'Cannot find model {app_label}.{model_name}.'.format(app_label=app_label, model_name=model_name)                     

            if history:
                # for the template, prepare separate ordered lists of field labels and field names
                field_labels = ['#','type', 'time', 'user'] + [
                                fld.name for fld in history[0]._meta.fields if fld.column[-3:]=='_id' and fld.name<>'_audit_id'] + [
                                fld.name for fld in history[0]._meta.fields if fld not in MyBasicModel._meta.fields and fld.name <> 'id' and fld.column[0]<>'_' and fld.column[-3:]<>'_id'] + [
                                fld.name for fld in MyBasicModel._meta.fields if fld.name <> 'user_modified']
                field_labels = [' '.join(name.split('_')) for name in field_labels]                    
                
                field_names = ['_audit_id','_audit_change_type', '_audit_timestamp', 'user_modified'] + [
                                fld.name for fld in history[0]._meta.fields if fld.column[-3:]=='_id' and fld.name<>'_audit_id'] + [
                                fld.name for fld in history[0]._meta.fields if fld not in MyBasicModel._meta.fields and fld.name <> 'id' and fld.column[0]<>'_' and fld.column[-3:]<>'_id'] + [
                                fld.name for fld in MyBasicModel._meta.fields if fld.name <> 'user_modified']

                # store values in a ordered list
                display_rows = []
                
                if audit_subject_identifier:
                    history_rows = model.history.filter(_audit_subject_identifier__icontains = audit_subject_identifier).order_by('_audit_timestamp')                
                else:    
                    history_rows = model.history.all().order_by('_audit_timestamp')
                                    
                for row in history_rows:
                    this_row = []
                    for field_name in field_names:
                        try:
                            # try if the field has a choices tuple, use get_FOO_display(), or fail
                            this_row.append(eval('row.get_'+field_name+'_display()'))                
                        except:
                            this_row.append(getattr(row, field_name))
                        
                    display_rows.append(this_row)
            else:
                status_message = 'There are no entries in the audit trail for this model.'                    
                
    else:
    
        form = AuditTrailForm(request.GET)
        app_label = request.GET.get('app_label', kwargs.get('app_label'))
        model_name = request.GET.get('model_name', kwargs.get('model_name'))
        audit_subject_identifier = request.GET.get('audit_subject_identifier', kwargs.get('audit_subject_identifier'))
        model_selector = ModelSelector(app_label, model_name)
        
        # these parameters are ugly, they couple to bhp_dashboard! Same in form and template
        back_url_name = request.GET.get('back_url_name', kwargs.get('back_url_name'))                                        
        dashboard_type = request.GET.get('dashboard_type', kwargs.get('dashboard_type'))
        visit_code = request.GET.get('visit_code', kwargs.get('visit_code'))
        visit_instance = request.GET.get('visit_instance', kwargs.get('visit_instance'))

               

    return render_to_response(template, { 
        'section_name': section_name, 
        'report_title': report_title, 
        'verbose_name': verbose_name,
        'history': history,
        'field_labels': field_labels,
        'field_names': field_names,
        'display_rows': display_rows,
        'form': form,
        'err_message': err_message,
        'status_message': status_message,        
        'app_label':app_label,
        'model_name': model_name,
        'audit_subject_identifier': audit_subject_identifier,
        'dashboard_type': dashboard_type,
        'visit_code':visit_code,
        'visit_instance': visit_instance,
        'back_url_name': back_url_name,
        'app_labels':model_selector.app_labels,
        'model_names': model_selector.model_names,
        }, context_instance=RequestContext(request))

