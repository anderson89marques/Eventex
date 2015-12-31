from django.test import TestCase
from eventx.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get("/inscricao/")

    def test_get(self):
        """ GET /inscricao/ must return status code 200  """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ GET /inscricao must return subscription_form.html """
        self.assertTemplateUsed(self.resp, "subscription/subscription_form.html")

    def test_html(self):
        """ html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input')
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_fields(self):
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))