from selenium.webdriver.common.by import By
from .base_page import BasePage


class HouseholdMemberPage(BasePage):
    first_name = (By.ID, 'id_first_name')
    initials = (By.ID, 'id_initials')
