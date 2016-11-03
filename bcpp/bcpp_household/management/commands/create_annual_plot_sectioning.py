from django.core.management.base import BaseCommand
from django.conf import settings

from bhp066.apps.bcpp_household.classes.notebook_plot_allocation import NotebookPlotAllocation


class Command(BaseCommand):

    args = ''
    help = 'Creates annual plot sectioning base on custom plot allocation plan for a particular community.'

    def handle(self, *args, **options):
        print ("Creating plot sectioning for {} - {}. This process takes few minutes.".format(
            settings.CURRENT_COMMUNITY, settings.CURRENT_SURVEY))
        plot_section = NotebookPlotAllocation()
        print("There are {} machines and generated section "
              "plan {} ".format(len(plot_section.community_hosts), plot_section.sections))
        print("")
        print("Plot sectioning ready.")
        print ()
        plot_section.update_sectioned_plots()
        print ("Dispatch is ready.")
