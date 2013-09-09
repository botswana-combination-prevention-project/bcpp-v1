from django.test import TestCase
from bhp_entry_rules.classes import BaseRule


class BaseRuleTests(TestCase):

    def test_get_operator_from_word(self):
        base_rule = BaseRule()
        self.assertRaises(TypeError, base_rule.get_operator_from_word, 'nathan', 1, [1, 2])
        self.assertEqual(base_rule.get_operator_from_word('eq', 1, 1), '==')
        self.assertEqual(base_rule.get_operator_from_word('==', 1, 1), '==')
        self.assertEqual(base_rule.get_operator_from_word('lt', 1, 1), '<')
        self.assertEqual(base_rule.get_operator_from_word('lte', 1, 1), '<=')
        self.assertEqual(base_rule.get_operator_from_word('gt', 1, 1), '>')
        self.assertEqual(base_rule.get_operator_from_word('gte', 1, 1), '>=')
        self.assertEqual(base_rule.get_operator_from_word('lt', 1, 1), '<')
        self.assertEqual(base_rule.get_operator_from_word('lte', 1, 1), '<=')
        self.assertEqual(base_rule.get_operator_from_word('ne', 1, 1), '!=')
        self.assertEqual(base_rule.get_operator_from_word('!=', 1, 1), '!=')
        self.assertEqual(base_rule.get_operator_from_word('in', 1, [1, 2]), 'in')
        self.assertEqual(base_rule.get_operator_from_word('not in', 1, [1, 2]), 'not in')
