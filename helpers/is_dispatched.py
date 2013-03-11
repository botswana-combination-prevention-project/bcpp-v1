#from bhp_dispatch.models import DispatchItem
#
#
#def is_dispatched(item_identifier):
#        """Returns dispatch status if the item based on the identifier."""
#        raise TypeError('Method is not used. Access the model method.')
#        locked = False
#        if DispatchItem.objects.filter(
#                item_identifier=item_identifier,
#                is_dispatched=True).exists():
#            locked = True
#        return locked
