import time

from .base_selinium_test import BaseSeleniumTest

from .pages import SearchPage, PlotResultPage, PlotLogEntryPage, PlotPage


class TestSearchPlotSeleniumTest(BaseSeleniumTest):

    def setUp(self):
        search_page = SearchPage
        plot_result_page = PlotResultPage
        plot_log_entry_page = PlotLogEntryPage
        plot_page = PlotPage

    def test_search_plot(self):
        self.login()
        time.sleep(1)
        self.plot_result_page.click_plotlink()
        time.sleep(1)
        self.search_page.search('400007-03')
        time.sleep(2)
        self.plot_result_page.click_addnewentry()
        time.sleep(1)
        self.plot_log_entry_page.fill_plot_log_entry()
        time.sleep(1)
        self.plot_result_page.get_plot('400007-03')
        time.sleep(1)
        self.plot_page.fill_plot_change('residential_habitable', 25, 25, 90, 25, 2)
