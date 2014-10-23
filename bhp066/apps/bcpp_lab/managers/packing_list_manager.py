from django.db.models import Manager


class PackingListManager(Manager):

    def get_by_natural_key(self, list_datetime):
        return self.get(list_datetime=list_datetime)


class PackingListItemManager(Manager):

    def get_by_natural_key(self, item_reference):
        return self.get(item_reference=item_reference)
