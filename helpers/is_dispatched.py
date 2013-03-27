from bhp_dispatch.models import DispatchContainerRegister


def is_dispatched(container_identifier):
    """Returns dispatch status if the item based on the container_identifier."""
    locked = False
    if DispatchContainerRegister.objects.filter(
            container_identifier=container_identifier,
            is_dispatched=True).exists():
        locked = True
    return locked
