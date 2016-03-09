import copy

from django.conf import settings
from bhp066.apps.bcpp_subject.models.subject_consent import SubjectConsent


class NotebookPlotAllocation(object):

    notebook_plot_lists = []

    def __init__(self, sectioned_plots=None):
        self.sectioned_plots = sectioned_plots
        self.community = settings.CURRENT_COMMUNITY

    @property
    def current_community_plot(self):
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
                host_plots.append(consent.household_member.household_structure.householdplot.plot_identifier)
            temp.append(host_plots)
            generated_plot_list.append(temp)
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
        for plots_data in self.allocate_sections:
            hostname, plots_identifiers, sections = plots_data
            for plot_identifier in plots_identifiers:
                hostname = hostname
                section, sub_section = sections
                plot = Plot.objects.get(plot_identifier=plot_identifier)
                plot.section = section
                plot.sub_section = sub_section
                plot.save(update_fields=['section', 'sub_section'])

    @property
    def allocate_sections(self):
        sectioned_plots = []
        plots = copy.deepcopy(self.allocated_shared_plots)
        j = 0
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
            notebook_list = copy.deepcopy(plots[1])
            for sub_list in all_plots:
                main_index = duplicate_plots_list.index(sub_list)
                try:
                    _sub_list = sub_list[1]
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
        path = '/Users/tsetsiba/source/bhp066_project/bhp066/apps/bcpp_household/annual_notebook_list/test_lerala.txt'
        self.file = open(path)
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
                    if shared_hosts:
                        for i, shared in enumerate(shared_hosts):
                            for shrd in shared:
                                if shrd == host:
                                    temp = shared_hosts[i]
                                    temp[1].append(hosts[0].strip())
                                    shared_hosts[i] = temp
                    else:
                        shared_hosts.append([host, [hosts[0]]])
        return shared_hosts

    @property
    def prepare_notebook_plot_list(self):
        final_notebook_plot_list = []
        for hosts in self.custom_allocation_config:
            host_to_be_assigned = hosts[0]
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
                    temp.append(host.strip())
                    tmp = shared_plots[i] + pl[1]
                    temp.append(tmp)
                    all_plots[x] = temp
        return all_plots

    @property
    def allocated_shared_plots(self):
        original_plots = self.remove_duplicates_and_load_balance_plots
        all_plots = copy.deepcopy(self.prepare_notebook_plot_list)
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
