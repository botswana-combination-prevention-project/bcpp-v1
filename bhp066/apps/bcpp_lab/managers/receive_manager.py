from django.db.models import Manager


class ReceiveManager(Manager):

    def get_by_natural_key(self, receive_identifier):
        return self.get(receive_identifier=receive_identifier)
