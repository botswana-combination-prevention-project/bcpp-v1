from ..constants import CONFIRMED
from ..models import Plot


def update_increaseplotradius():
    num_created = 0
    for plot in Plot.objects.filter(selected__isnull=False).exclude(action=CONFIRMED):
        _, created = plot.increase_plot_radius
        if created:
            num_created += 1
    return num_created
