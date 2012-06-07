from bhp_base_model.classes import BaseListModel


class MyBasicListModel(BaseListModel):

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering=['display_index']


