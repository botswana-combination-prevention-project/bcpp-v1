from django.db.models import Q
from bhp_research_protocol.models import Protocol
from lab_receive.models import Receive
from lab_order.models import Order
from import_history import ImportHistory


class Lis(object):

    """ Import from django-lis"""
    def __init__(self, db, **kwargs):
        self.db = db

    def import_from_lis(self, protocol_identifier=None, **kwargs):

        import_history = ImportHistory(self.db, kwargs.get('subject_identifier', None) or protocol_identifier)
        if import_history.start():
            # import all received
            protocol = Protocol.objects.using(self.db).get(protocol_identifier__iexact=protocol_identifier)
            qset = Q(protocol=protocol)
            if import_history.last_import_datetime:
                qset.add(Q(modified__gte=import_history.last_import_datetime) | Q(created__gte=import_history.last_import_datetime))
            for lis_receive in Receive.objects.using(self.db).filter(qset):
                if not import_history.locked:
                    # lock was deleted by another user
                    break
                receive = Receive()
                for field in lis_receive._meta.fields:
                    setattr(receive, field.attname, getattr(field, field.attname))
                receive.save()
        import_history.finish()
        return None
