from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Anderson Marques", cpf="00644321229", email="andersonoanjo18@mailinator.com", phone="984593967")
        self.client.post(r('subscription:new'), data)
        self.email = mail.outbox[0]

    def test_subscribe_email_subject(self):
        self.assertEqual("Confirmação de inscrição", self.email.subject)

    def test_subscribe_email_from(self):
        self.assertEqual("andersonoanjo18@gmail.com", self.email.from_email)

    def test_subscribe_email_to(self):
        expect = ["andersonoanjo18@mailinator.com"]
        self.assertEqual(expect, self.email.to)

    def test_subscribe_email_body(self):
        contents = ["Anderson Marques", "00644321229", "andersonoanjo18@mailinator.com", "984593967"]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)