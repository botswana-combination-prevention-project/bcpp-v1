from selenium.webdriver.common.by import By
from .base_page import BasePage


class SearchPage(BasePage):
    keyword = (By.ID, 'id_search_term')
    search_button = (By.XPATH, "//input[@type='submit' and @value='Search']")

    def set_keyword(self, keyword):
        keywordElement = self.browser.find_element(*SearchPage.keyword)
        keywordElement.send_keys(keyword)

    def click_search(self):
        self.browser.find_element(*SearchPage.search_button).click()

    def search(self, keyword):
        self.set_keyword(keyword)
        self.click_search()
