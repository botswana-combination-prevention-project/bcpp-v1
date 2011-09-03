from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from lab_requisition.classes import ClinicRequisitionLabel


@login_required
def ajax_print( request, requisition_identifier, requisition_model ):

    if request.is_ajax():
        if requisition_identifier is not None:            
            requisition = requisition_model.objects.get(requisition_identifier = requisition_identifier)
            
            for cnt in range(self.item_count_total, 0, -1):
                label = ClinicRequisitionLabel(
                                item_count = cnt, 
                                requisition = self,
                                )
                label.print_label() 
    return None                

