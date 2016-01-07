from datetime import datetime

from django.test import TestCase
from eventx.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name="Anderson Marques",
            cpf="00644321229",
            email="andersonoanjo18@gmail.com",
            phone="984593967"
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual("Anderson Marques", str(self.obj))
