from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured


class NotebookPlotAllocation(object):

    notebook_plot_lists = []

    def __init__(self, notebook_plot_list=None, num_of_machines=None):
        self.notebook_plot_list = notebook_plot_list
        self.num_of_machines = num_of_machines
        self._notebook_plot_allocation_list = []
        self.total = 0
        self.notebook_plot_list = self.flatten_plots

    @property
    def remainder(self):
        """Find the remainder using modulus.
            Args:
                None
            Returns:
                if a list contains odd number of items counts then remainder otherwise 0.  """
        return len(self.notebook_plot_list) % self.num_of_machines

    @property
    def flatten_plots(self):
        """Converts Plot Instance into a list of plot identifier strings.
            Args:
                None
            Returns:
                A list of plot identifiers """
        return [pi.plot_identifier for pi in self.notebook_plot_list]

    @property
    def distributed_notebook_plot_list(self):
        """"Distributes plots based on numbers of machines available.
        Args:
            None
        Returns:
            Returns a list of dictionary for plot identifiers based on numbers of machines to allocates plots to.
        """
        x = self.num_of_machines
        y = len(self.notebook_plot_list) / x  # plot allocation numbers
        z = self.notebook_plot_list  # notebook plot list
        u = y + 1  # number of iteration
        for i in range(1, u):
            self.total = y * i
            prev = self.total - y  # previous number or last index
            j = u - 1
            if j == i:
                self._notebook_plot_allocation_list.append(dict(machine_plots=z[prev:self.total]))
                if not self.remainder == 0:
                    self.total = len(self.notebook_plot_list)
                    prev = self.total - y
                    self.total = self.total + self.remainder
                    self.distribute_remainder(prev)
                    break
            else:
                self._notebook_plot_allocation_list.append(dict(machine_plots=z[prev:self.total]))

        return self._notebook_plot_allocation_list

    def distribute_remainder(self, previous_index):
        """Distributes remainder across lists created for each popular machine.
            Args:
                previous_index: if there are 3 plots all together the previous index will be 2.
            Returns:
                A complete distributed list of dictionary notebook plot list for each machines.
        """
        prev = previous_index
        for q in range(0, self.remainder):
            tmp_list = self._notebook_plot_allocation_list[q].get('machine_plots')
            tmp_list.append(self.notebook_plot_list[prev + q])
            self._notebook_plot_allocation_list[q] = dict(machine_plots=tmp_list)

    def machine_notebook_plot_list(self, slot):
        """A list of plot identifier for each particular machine.
            Args:
                slot: if there are 5 machines they will be five slots.
            Returns:
                A list of plots in a particular index or slot.
        """
        return self._notebook_plot_allocation_list[slot].get('machine_plots')

    def create_notebook_plot_list(self, slot):
        """Create a notebook plot list in database.
            Args:
                slot: index for particular plots
            Returns:
                None
        """
        if slot > self.num_of_machines:
            raise ImproperlyConfigured('Provide correct slot, out of index.')
        NotebookPlotList = get_model('bcpp_household', 'notebookplotlist')
        for plot_identifier in self._notebook_plot_allocation_list[slot]['machine_plots']:
            if not NotebookPlotList.objects.filter(plot_identifier=plot_identifier):
                NotebookPlotList.objects.create(plot_identifier=plot_identifier)
