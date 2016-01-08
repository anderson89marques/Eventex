from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventx.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        obj = Subscription.objects.create(name="Anderson Marques", cpf="00644321229",
                                          email="andersonoanjo18@mailinator.com", phone="984593967")

        self.resp = self.client.get(r('subscription:detail', obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, "subscription/subscription_detail.html")

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = ("Anderson Marques", "00644321229", "andersonoanjo18@mailinator.com", "984593967")
        for content in contents:
            with self.subTest():
                self.assertContains(self.resp, content)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        self.resp = self.client.get(r('subscription:detail', 0))
        self.assertEqual(404, self.resp.status_code)