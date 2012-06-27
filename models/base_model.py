try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
    

class BaseModel(BaseUuidModel):
        
        class Meta:
            abstract = True