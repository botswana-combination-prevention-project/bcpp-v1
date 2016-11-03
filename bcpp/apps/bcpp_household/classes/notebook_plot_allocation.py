import copy

from django.conf import settings
from django.db.models import Q

from bhp066.apps.bcpp_subject.models.subject_consent import SubjectConsent
from bhp066.apps.bcpp_household.models import Plot


class NotebookPlotAllocation(object):

    notebook_plot_lists = []

    def __init__(self, sectioned_plots=None):
        self.path = None
        self.community = settings.CURRENT_COMMUNITY
        self.sectioned_plots = sectioned_plots or self.current_community_plot

    def not_allocated_plots(self):
        pass

    @property
    def current_community_plot(self):
        print ("Generating plot allocation using given custom plot allocation config file.")
        generated_plot_list = []
        for host in self.filtering_hosts:
            hostname_created = host.strip()
            consents = SubjectConsent.objects.filter(
                hostname_created=hostname_created,
                household_member__household_structure__household__plot__community=self.community)
            temp = []
            temp.append(hostname_created)
            host_plots = []
            for consent in consents:
                if not (consent.household_member.household_structure.household.plot.plot_identifier in host_plots):
                    host_plots.append(consent.household_member.household_structure.household.plot.plot_identifier)
            temp.append(host_plots)
            generated_plot_list.append(temp)
        if len(generated_plot_list) > 1:
            print("Plot allocation is ready.")
        return generated_plot_list

    @property
    def sections(self):
        sub_section = []
        number_of_hosts = len(self.community_hosts)
        number = number_of_hosts / 3
        for section in ['A', 'B', 'C']:
            temp = []
            if not number_of_hosts % 3 == 0:
                if section == 'C':
                    number = number + number_of_hosts % 3
                    temp.append(section)
                    temp.append(number)
                    sub_section.append(temp)
                else:
                    temp.append(section)
                    temp.append(number)
                    sub_section.append(temp)
            else:
                temp.append(section)
                temp.append(number)
                sub_section.append(temp)
        return sub_section

    def update_sectioned_plots(self):
        updated_plots = []
        for plots_data in self.allocate_sections:
            hostname, plots_identifiers, sections = plots_data
            print("{} has been allocated {} plot(s).".format(hostname, len(set(plots_identifiers))))
            for plot_identifier in list(set(plots_identifiers)):
                hostname = hostname
                section, sub_section = sections
                plot = Plot.objects.get(plot_identifier=plot_identifier)
                plot.section = section
                plot.sub_section = sub_section
                plot.save(update_fields=['section', 'sub_section'])
                updated_plots.append(plot_identifier)
        print("{} plot(s) has been sectioned.".format(len(list(set(updated_plots)))))
        print("Determing plots which are not allocated and sectioned.")
        consents = SubjectConsent.objects.filter(
            ~Q(household_member__household_structure__household__plot__plot_identifier__in=updated_plots))
        machines = list(set(consents.values_list('hostname_created')))
        number_of_plots = consents.values_list(
            'household_member__household_structure__household__plot__plot_identifier')
        print ("There are {} for these "
               "machines -({}) not "
               "allocated.".format(len(list(set(consents.values_list('hostname_created')))), machines))
        print ("Overall number of plots not being allocated: {}.".format(list(set(number_of_plots))))
        return updated_plots

    @property
    def allocate_sections(self):
        sectioned_plots = []
        plots = copy.deepcopy(self.allocated_shared_plots)
        j = 0
        if plots:
            print("Allocating generated sectioning.")
        for sections in self.sections:
            section = sections[0]
            sub_section = 0
            for sub_sections in range(sections[1]):
                sub_section = sub_sections + 1
                temp = plots[j]
                temp.append([section, sub_section])
                sectioned_plots.append(temp)
                j = j + 1
        return sectioned_plots

    @property
    def remove_duplicates_and_load_balance_plots(self):
        duplicate_plots_list = self.sectioned_plots
        i = 0
        for plots in duplicate_plots_list:
            all_plots = copy.deepcopy(duplicate_plots_list)
            all_plots.remove(plots)
            _plots = list(set(plots[1]))
            notebook_list = copy.deepcopy(list(set(plots[1])))
            for sub_list in all_plots:
                main_index = duplicate_plots_list.index(sub_list)
                try:
                    _sub_list = list(set(sub_list[1]))
                    for identifier in _plots:
                        if identifier in list(set(_sub_list)):
                            if len(set(duplicate_plots_list[main_index][1])) >= len(notebook_list):
                                searched_notebook_list = list(set(duplicate_plots_list[main_index][1]))
                                searched_notebook_list.remove(identifier)
                                temp = []
                                temp.append(sub_list[0].strip())
                                temp.append(searched_notebook_list)
                                duplicate_plots_list[main_index] = temp
                            else:
                                notebook_list.remove(identifier)
                except IndexError as err:
                    print err
            if not len(duplicate_plots_list[i][1]) == len(notebook_list):
                temp = []
                temp.append(plots[0].strip())
                temp.append(notebook_list)
                duplicate_plots_list[i] = temp
            else:
                duplicate_plots_list[i] = plots
            i = i + 1
        return duplicate_plots_list

    @property
    def current_community_config_file(self):
        hosts = []
        if self.path is None:
            raise (
                "Specific the distribution config file for the current community-{}".format(settings.CURRENT_COMMUNITY))
        self.file = open(self.path)
        for line in self.file.readlines():
            hosts.append(line.strip())
        return hosts

    @property
    def filtering_hosts(self):
        available_hosts = []
        for host in self.current_community_config_file:
            _host = host.split('<')[1]
            if '&' in _host:
                _host = _host.split('&')
                for hostname in _host:
                    if 'half' in hostname:
                        if not (hostname.strip()[:7] in available_hosts):
                            available_hosts.append(hostname.strip()[:7])
                    else:
                        if not (hostname in available_hosts):
                            available_hosts.append(hostname.strip())
            else:
                if not (_host in available_hosts):
                    available_hosts.append(_host.strip())
        return list(set(available_hosts))

    @property
    def custom_allocation_config(self):
        available_hosts = []
        for host in self.current_community_config_file:
            temp = []
            temp.append(host.split('<')[0])
            _host = host.split('<')[1]
            if '&' in _host:
                _host = _host.split('&')
                for hostname in _host:
                    temp.append(hostname.strip())
            else:
                temp.append(_host.strip())
            available_hosts.append(temp)
        return available_hosts

    @property
    def custom_allocation_config_shared(self):
        shared_hosts = []
        for hosts in self.custom_allocation_config:
            for host in hosts:
                if 'half' in host:
                    temp = []
                    temp.append(host)
                    if not (temp in shared_hosts):
                        shared_hosts.append(temp)

        for x, shared_host in enumerate(shared_hosts):
            sharing_hosts = []
            for hosts in self.custom_allocation_config:
                if shared_host[0] in hosts:
                    sharing_hosts.append(hosts[0])
            shared_hosts[x].append(sharing_hosts)
        return shared_hosts

    @property
    def prepare_notebook_plot_list(self):
        final_notebook_plot_list = []
        for hosts in self.custom_allocation_config:
            host_to_be_assigned = hosts[0].strip()
            hosts_to_allocated = hosts[1:]
            temp = []
            temp.append(host_to_be_assigned)
            for host in hosts_to_allocated:
                if not ('half' in host):
                    for plots in self.remove_duplicates_and_load_balance_plots:
                        if host == plots[0]:
                            if len(temp) > 1:
                                temp[1] = temp[1] + plots[1]
                            else:
                                temp.append(plots[1])
            final_notebook_plot_list.append(temp)
        return final_notebook_plot_list

    def distribute_shared_plots(self, all_plots, sharing_hosts, shared_plots):
        for i, host in enumerate(sharing_hosts):
            for x, pl in enumerate(all_plots):
                temp = []
                if host.strip() == pl[0].strip():
                    try:
                        pl = pl[1] if len(pl) > 1 else []
                        temp.append(host.strip())
                        tmp = shared_plots[i] + pl
                        temp.append(tmp)
                        all_plots[x] = temp
                    except IndexError:
                        print ("Error trying to allocate shared plots for {}".format(host))
        return all_plots

    @property
    def allocated_shared_plots(self):
        original_plots = self.remove_duplicates_and_load_balance_plots
        all_plots = copy.deepcopy(self.prepare_notebook_plot_list)
        if all_plots:
            print("Plot duplication across the machines has been removed.")
        for shared in self.custom_allocation_config_shared:
            shared_hostname = shared[0].strip()[:7]
            sharing_hosts = shared[1]
            first_half = []
            remaining_half = []
            shared_plots = []
            for plots in original_plots:
                if shared_hostname == plots[0]:
                    h = len(plots[1]) / 2
                    first_half = plots[1][:h]
                    remaining_half = plots[1][h:]
                    shared_plots.append(first_half)
                    shared_plots.append(remaining_half)
            all_plots = self.distribute_shared_plots(all_plots, sharing_hosts, shared_plots)
        return all_plots

    @property
    def community_notebook_plot_list(self):
        return self.allocated_shared_plots

    @property
    def community_hosts(self):
        all_hosts = []
        for host in self.current_community_config_file:
            all_hosts.append(host.split('<')[0].strip())
        return all_hosts
