from django.core.urlresolvers import reverse
    
def check_dashboard_redirect(result, request, next_named_url, **kwargs ):   

    """ Check for redirect to the named dashboard.
    
    put in admin ModelAdmin change_view. In the example, the consent
    comes from the current model (MaternalEligibilityAnte) using the
    object_id
    
    def change_view(self, request, object_id, extra_context=None):

        result = super(MaternalEligibilityAnteAdmin, self).change_view(request, object_id, extra_context)
        
        if request.GET.get('next'):
            # get subject_identifier
            subject_identifier = MaternalEligibilityAnte.objects.get(pk = object_id).maternal_consent.subject_identifier
            # get redirect
            result = check_dashboard_redirect(result, request, subject_identifier, 
                next_named_url = request.GET.get('next'), 
                dashboard_name = request.GET.get('dashboard'),)
                
        return result     

    
    """
    

    if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
        if request.GET.get('next') == next_named_url :
            result['Location'] = reverse(request.GET.get('next'), kwargs=kwargs )

    return result 
