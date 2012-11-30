from datetime import datetime
from bhp_dispatch.models import DispatchItem
from bhp_dispatch.classes import DispatchHelper


def process_dispatch(modeladmin, request, queryset, **kwargs):

    """Checkout all selected households to specified netbooks.
    
    Acts on the 

    Algorithm
    for each Dispatch instance:
        get a list of household identifiers
            foreach household identifier
                create a DispatchItem
                set the item as Dispatch
                set the checkout time to now
                invoke controller.checkout (...) checkout the data to the netbook
        update Dispatch instance as checked out
    """
    if len(queryset):
        helper = DispatchHelper(True)
    else:
        pass
    for qs in queryset:
        # Make sure the checkout instance is not already checked out and has not been checked back again
        if qs.is_checked_out == True and qs.is_checked_in == False:
            raise ValueError("There are households already checked to {0} that have not been checked back in!".format(qs.producer.name))
        else:
            # item identifiers are separated by new lines, so explode them on "\n"
            item_identifiers = qs.checkout_items.split()
            for item_identifier in item_identifiers:
                # Save to producer
                helper.checkout(item_identifier, qs.producer.name)
                # create dispatch item
                DispatchItem.objects.create(
                    producer=qs.producer,
                    hbc_dispatch=qs,
                    item_identifier=item_identifier,
                    is_checked_out=True,
                    datetime_checked_out=datetime.today())
                modeladmin.message_user(
                    request, 'Checkout {0} to {1}.'.format(item_identifier, qs.producer))
            qs.datetime_checked_out = datetime.today()
            qs.is_checked_out = True
            qs.save()
            modeladmin.message_user(request, 'The selected items were successfully checkout to \'{0}\'.'.format(qs.producer))
