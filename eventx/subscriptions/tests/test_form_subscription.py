from django.test import TestCase
from eventx.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def setUp(self):
        self.form = SubscriptionForm()

    def test_has_fields(self):
        expect = ['name', 'cpf', 'email', 'phone']

        self.assertSequenceEqual(expect, list(self.form.fields))