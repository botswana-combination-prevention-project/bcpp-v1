from bhp_base_model.classes import BaseUuidModel


class BaseModel(BaseUuidModel):

        class Meta:
            abstract = True
