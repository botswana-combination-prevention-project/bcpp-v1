from bhp_base_model.models import BaseListModel


class MyBasicListModel(BaseListModel):

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['display_index']
