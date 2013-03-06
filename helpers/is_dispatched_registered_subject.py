from bhp_dispatch.models import DispatchItem


def is_dispatched_registered_subject(registered_subject):
    """Returns lock status and producer as a tuple for the "pk" of the given registered subject."""
    locked = False
    producer = None
    raise TypeError('Method is not used. Access the model method.')
    if DispatchItem.objects.filter(
            subject_identifiers__icontains=registered_subject.pk,
            is_dispatched=True).exists():
        dispatch_item = DispatchItem.objects.get(
            subject_identifiers__icontains=registered_subject.pk,
            is_dispatched=True)
        producer = dispatch_item.producer
        locked = True
    return locked, producer
