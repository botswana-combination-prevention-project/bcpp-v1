from selenium import webdriver

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.utils import timezone

from ..bcpp_household.models import Plot
from ..bcpp_household.tests.factories import PlotFactory

from .pages.login_page import LoginPage


class BaseSeleniumTest(LiveServerTestCase):

    username = 'testuser'
    password = '12345'
    email = 'testuser@123.org'

    def setUp(self):
        self.user = User.objects.create_superuser('testuser', self.email, self.password)
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        self.create_plots()

#     def tearDown(self):
#         self.browser.close()

    def login(self):
        self.login_page = LoginPage(self.browser)
        self.login_page.login(self.username, self.password)

    def create_plots(self):
        plot = Plot.objects.create(
            id="0022e2a1-81c0-4176-93e8-a5028cdfa8cd",
            comment=None,
            hostname_created="silverapple",
            htc=False,
            gps_target_lat="-23.020879019",
            hostname_modified="silverapple",
            community="gumare",
            cso_number=None,
            user_created="",
            time_of_week=None,
            gps_target_lon="27.5208530588",
            bhs=None,
            enrolled_datetime=None,
            access_attempts=0,
            section="D",
            selected="1",
            user_modified="",
            target_radius=0.025,
            revision="master:3f8edfac1fbd93c4d78c1b1f8728377015368b46",
            status=None,
            gps_lat=None,
            description=None,
            gps_degrees_e=None,
            replaceable=None,
            distance_from_target=None,
            gps_lon=None,
            eligible_members=None,
            replaced_by=None,
            sub_section=None,
            device_id=None,
            gps_minutes_s=None,
            gps_degrees_s=None,
            replaces=None,
            created=timezone.now(),
            household_count=0,
            modified=timezone.now(),
            plot_identifier="391617-06",
            time_of_day=None,
            uploaded_map_18=None,
            gps_minutes_e=None,
            action="unconfirmed",
            uploaded_map_17=None,
            uploaded_map_16=None,
        )
        print (Plot.objects.all()[0].__dict__)
