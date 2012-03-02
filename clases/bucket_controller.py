
class ModelBucket(object):

    def __init__(self, **kwargs):
        
        self.actions = kwargs
        

class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass       
 
class BucketController(object):
    
    def __init__(self):
    
        self._registry = {}
    
    def register(self, model, model_bucket): 
            
        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)
        
        self._registry[model] = model_bucket
        
    def update(self, instance):
        
        for model, model_bucket in self._registry.iteritems():
            if instance.__class__ == model:
                for action in model_bucket.actions:
                    action.run(instance)
                raise TypeError(self._registry)
    
        
bucket = BucketController()        