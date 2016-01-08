from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventx.subscriptions.forms import SubscriptionForm
from eventx.subscriptions.models import Subscription


class SubscriptionNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscription:new'))

    def test_get(self):
        """ GET /inscricao/ must return status code 200  """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ GET /inscricao must return subscription_form.html """
        self.assertTemplateUsed(self.resp, "subscription/subscription_form.html")

    def test_html(self):
        """ html must contain input tags"""

        tags = (("<form", 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1)
                )

        for tag, count in tags:
            with self.subTest():
                self.assertContains(self.resp, tag, count)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionNewPostValid(TestCase):
    def setUp(self):
        data = dict(name="Anderson Marques", cpf="00644321229", email="andersonoanjo18@mailinator.com", phone="984593967")
        self.resp = self.client.post(r('subscription:new'), data)

    def test_redirect_post(self):
        """ Após a requisição o usuário deve ser redirecionado para inscricao/1/ """
        obj = self.resp.context['subscription']
        self.assertRedirects(self.resp, r('subscription:detail', obj.pk))

    def test_send_email(self):
        """ Deve ser enviando um email de confirmação de inscricao """

        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscription:new'), {})

    def test_invalid_post(self):
        """ Invalid POST should not redirect """

        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.resp, "subscription/subscription_form.html")

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())