#import re
from django.db.models import Q
from hasher import Hasher


class CryptoQ(Q):
    
    """ Check for queries made against encrypted models fields and encrypt value """
    
    hasher = Hasher()
    
    def __init__(self, *args, **kwargs):
                
        # intercept lookups on an encrypted field
        cust_lookups = filter(lambda s: s[0].endswith('__hash'), kwargs.items())
        for lookup in cust_lookups:
            kwargs.pop(lookup[0])
            lookup_prefix = lookup[0].rsplit('__',1)[0]
            kwargs.update({lookup_prefix + '__contains':self.hasher.get_hash(lookup[1])})
            
        super(Q, self).__init__(children=list(args) + kwargs.items())
        