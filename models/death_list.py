from bhp_base_model.models import BaseListModel


class DeathCauseInfo (BaseListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'bhp_adverse'


class DeathCauseCategory (BaseListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'bhp_adverse'


class DeathMedicalResponsibility (BaseListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'bhp_adverse'


class DeathReasonHospitalized (BaseListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'bhp_adverse'
