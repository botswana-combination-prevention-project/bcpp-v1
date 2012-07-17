from model_rule import ModelRule


class ModelBucket(object):
    
    """ Container for :class:`ModelRule` for a given model bucket.
    
    ModelBuckets are contained by the BucketController
    """
    
    def __setitem__(self, name, model_rule):
        
        if not isinstance(model_rule, ModelRule):
            raise AttributeError('%s expects attribute \'%s\' to be instance of ModelRule.' % (self, model_rule))
        
        if not self[name]:
            self[name] = model_rule
        raise TypeError()
        
        return object.__setitem__(self, name, model_rule)
    
    def __delattr__(self, name):
        
        if self.model_rules[name]:
            del self.model_rules[name]
        
        return object.__delattr__(self, name)

    def __iter__(self):
        return iter(self.model_rules)
     
    def __next__(self):
        while self.index < len(self.model_rules):
            yield self.model_rules[self.index]
            self.index += 1   
    
    def count(self):
        return len(self.model_rules)
    
