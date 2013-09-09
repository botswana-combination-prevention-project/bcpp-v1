
def set_is_dispatched(modeladmin, request, queryset, **kwargs):
    """Sets is dispatched to True"""
    for qs in queryset:
        if qs.is_dispatched == False:
            qs.is_dispatched = True
            qs.return_datetime = None
            qs.save()
set_is_dispatched.short_description = "Set is_dispatched to True."
#def process_dispatch(modeladmin, request, queryset, **kwargs):
#
#    """Checkout all selected households to specified netbooks.
#    
#    Acts on the 
#
#    Algorithm
#    for each Dispatch instance:
#        get a list of household identifiers
#            foreach household identifier
#                create a DispatchItem
#                set the item as Dispatch
#                set the checkout time to now
#                invoke controller.checkout (...) checkout the data to the netbook
#        update Dispatch instance as checked out
#    """
#    if len(queryset):
#        dispatch_helper = DispatchHelper(True)
#    else:
#        pass
#    for qs in queryset:
#        # Make sure the checkout instance is not already checked out and has not been checked back again
#        if qs.is_dispatched == True:
#            raise ValueError("There are households in the list currently dispatched to {0}.".format(qs.producer.name))
#        else:
#            # item identifiers are separated by new lines, so explode them on "\n"
#            item_identifiers = qs.dispatch_items.split()
#            for item_identifier in item_identifiers:
#                # Save to producer
#                dispatch_helper.dispatch(item_identifier, qs.producer.name)
#                # create dispatch item
#                DispatchItem.objects.create(
#                    producer=qs.producer,
#                    dispatch=qs,
#                    item_identifier=item_identifier,
#                    is_dispatched=True,
#                    dispatched_datetime=datetime.today())
#                modeladmin.message_user(
#                    request, 'Dispatch {0} to {1}.'.format(item_identifier, qs.producer))
#            qs.dispatched_datetime = datetime.today()
#            qs.is_dispatched = True
#            qs.save()
#            modeladmin.message_user(request, 'The selected items were successfully dispatched to \'{0}\'.'.format(qs.producer))
