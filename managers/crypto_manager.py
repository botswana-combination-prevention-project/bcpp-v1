#from django.db import models
#from bhp_crypto.classes import Hasher
#
#
#class CryptoQuerySet(models.query.QuerySet):
#    
#    hasher = Hasher()
#    
#    def _filter_or_exclude(self, negate, *args, **kwargs):
#        
#        cust_lookups = filter(lambda s: s[0].endswith('__hash'), kwargs.items())
#        for lookup in cust_lookups:
#            kwargs.pop(lookup[0])
#            lookup_prefix = lookup[0].rsplit('__',1)[0]
#            kwargs.update({lookup_prefix + '__contains':self.hasher.get_hash(lookup[1]).hexdigest()})
#        return super(CryptoQuerySet, self)._filter_or_exclude(negate, *args, **kwargs)
#    
#    
#class CryptoManager(models.Manager):
#    
#    def get_query_set(self):
#        return CryptoQuerySet(self.model)