from django.db.models import Manager


class AliquotProcessingManager(Manager):

    def get_by_natural_key(self, aliquot_identifier, profile_name):
        return self.get(aliquot__aliquot_identifier=aliquot_identifier,profile__name=profile_name)