from django.db.models import get_models
from bhp_consent.models import BaseConsent


class SearchModels(object):

    def __init__(self):
        self.search_models = {}
        for model in get_models('bcpp_subject'):
            if isinstance(model, BaseConsent):
                self.search_models.update(model.object_name.lower(), model)
            if 'registered_subject' in dir(model):
                self.search_models.update(model.object_name.lower(), model)
