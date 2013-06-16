from django.test import TestCase
from django.core.paginator import Page
from bhp_consent.models import TestSubjectConsent
from bhp_consent.tests.factories import TestSubjectConsentFactory
from bhp_search.classes import BaseSearchByWord
from bhp_search.exceptions import SearchError, SearchModelError, SearchAttributeError


class SearchMethodsTests(TestCase):

    def test_section_name(self):

        class TestSearchByWord(BaseSearchByWord):
            section_name = 'subject'
            search_model = TestSubjectConsent

        test_search = TestSearchByWord()
        print 'assert returns section name from class variable'
        self.assertEqual(test_search.get_section_name(), 'subject')
        print 'assert returns search model from class variable as model class'
        self.assertTrue(issubclass(test_search.get_search_model_cls(), TestSubjectConsent))
        test_search = None
        TestSearchByWord.search_model = ('bhp_consent', 'TestSubjectConsent')
        test_search = TestSearchByWord()
        print 'assert returns search model from class variable as tuple'
        self.assertTrue(issubclass(test_search.get_search_model_cls(), TestSubjectConsent))
        TestSearchByWord.search_model = ('bhp_consentXXXX', 'TestSubjectConsent')
        error_test_search = TestSearchByWord()
        print 'assert raises error if cannot get a model class from class variable tuple'
        self.assertRaises(SearchModelError, error_test_search.get_search_model_cls)
        TestSearchByWord.section_name = None
        TestSearchByWord.search_model = ('bhp_consent', 'TestSubjectConsent')
        error_test_search = TestSearchByWord()
        print 'assert raises exception if class variable section_name not set'
        self.assertRaises(SearchAttributeError, error_test_search.get_section_name)
        print 'create 15 instances in the search model'
        i = 0
        while i < 15:
            TestSubjectConsentFactory()
            i += 1
        print 'get most recent (10)'
        self.assertIsNotNone(test_search.get_most_recent())
        obj = test_search.get_most_recent()
        print 'assert get_most_recent returns a paginator'
        self.assertTrue(isinstance(obj, Page))
