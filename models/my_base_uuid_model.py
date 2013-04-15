from bhp_consent.models import BaseConsentedUuidModel


class MyBaseUuidModel(BaseConsentedUuidModel):

    """ Base model for all maternal models """

    class Meta:
        abstract = True
