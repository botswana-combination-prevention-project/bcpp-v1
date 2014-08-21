import os

from datetime import datetime

from selenium.webdriver.firefox.webdriver import WebDriver

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.visit_schedule.models import VisitDefinition

from ..models import SubjectConsent


class SeleniumTests(LiveServerTestCase):

    fixtures = ['bhp_visit.json',
                'bhp_entry.json']

    def setUp(self):
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        # prepare the consent catalogue
        content_type_map = ContentTypeMap.objects.get(model__iexact=SubjectConsent._meta.object_name)
        ConsentCatalogueFactory(
            name='bcpp',
            content_type_map=content_type_map,
            consent_type='study',
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app='bcpp_subject')
        self.adminuser = User.objects.create_user('django', 'django@test.com', 'pass')
        self.adminuser.save()
        self.adminuser.is_staff = True
        self.adminuser.is_active = True
        self.adminuser.is_superuser = True
        self.adminuser.save()
        self.logged_in = False
        self.login()

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def login(self):
        # First check for the default behavior
        self.selenium.get('%s%s' % (self.live_server_url, '/erik/'))
        #self.assertRedirects(response, '/mochudi_survey/')
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('django')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('pass')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        self.selenium.get('%s%s' % (self.live_server_url, '/bcpp/'))
        self.logged_in = True

    def test_export(self):
        print 'set the visit definition to TO'
        self.set_visit_definition('TO')
        path = settings.MEDIA_ROOT
        self.assertFalse(VisitDefinition.objects.all().count() == 0)
        for entry in self.get_visit_definition().entry_set.all().order_by('entry_order'):
            model_class = entry.content_type_map.model_class()
            #model_admin = admin.site._registry.get(model_class)
            url = reverse('admin:{0}_{1}_add'.format(model_class._meta.app_label, model_class._meta.object_name.lower()))
            response = self.selenium.get('%s%s' % (self.live_server_url, url))
            response.
            #if not t.status_code == 200:
            #    raise TypeError('failed for model {0}. Got status_code {1}'.format(model_class, t.status_code))
            #content = t.render()
            fn = '{0}.html'.format(model_class._meta.object_name.lower())
            path = os.path.join(settings.MEDIA_ROOT, fn)
            fo = open(path, 'w')
            fo.write(content.rendered_content)
            fo.close()

    def set_visit_definition(self, code):
        self._visit_definition = VisitDefinition.objects.get(code=code)

    def get_visit_definition(self):
        if not self._visit_definition:
            self.set_visit_definition()
        return self._visit_definition
