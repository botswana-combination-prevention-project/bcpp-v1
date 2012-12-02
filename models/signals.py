#from dispatch import Dispatch
#
#
#def deserialize_from_signal(self, sender, incoming_transaction, **kwargs):
#    """ decrypt and deserialize the incoming json object"""
#    allow = True
#    #Dispatch = get_model('bhp_dispatch', 'Dispatch')
#    if Dispatch:
#        if not Dispatch.objects.filter(producer=incoming_transaction.producer):
#            allow = False
#    if allow:
#        self.deserialize(incoming_transaction)
