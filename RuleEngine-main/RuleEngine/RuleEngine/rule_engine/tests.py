from django.test import TestCase

# Create your tests here.

from .utils import create_rule, evaluate_rule

class RuleEngineTests(TestCase):
    def test_create_rule(self):
        rule = "((age > 30 AND department = 'Sales') AND salary > 50000)"
        ast_root = create_rule(rule)
        self.assertIsNotNone(ast_root)

    def test_evaluate_rule(self):
        rule = "((age > 30 AND department = 'Sales') AND salary > 50000)"
        ast_root = create_rule(rule)
        data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        result = evaluate_rule(ast_root, data)
        self.assertTrue(result)

        data = {"age": 25, "department": "Marketing", "salary": 40000, "experience": 1}
        result = evaluate_rule(ast_root, data)
        self.assertFalse(result)


