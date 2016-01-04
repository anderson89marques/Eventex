from django.core import mail
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


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name="Anderson Marques", cpf="00644321229", email="andersonoanjo18@mailinator.com", phone="984593967")
        self.resp = self.client.post("/inscricao/", data)

    def test_redirect_post(self):
        """ Após a requisição o usuário deve ser redirecionado para inscricao/ """

        self.assertEqual(302, self.resp.status_code)

    def test_send_email(self):
        """ Deve ser enviando um email de confirmação de inscricao """

        self.assertEqual(1, len(mail.outbox))

    def test_subscribe_email_subject(self):
        email = mail.outbox[0]
        self.assertEqual("Confirmação de inscrição", email.subject)

    def test_subscribe_email_from(self):
        email = mail.outbox[0]
        self.assertEqual("andersonoanjo18@gmail.com", email.from_email)

    def test_subscribe_email_to(self):
        email = mail.outbox[0]
        expect = ["andersonoanjo18@mailinator.com"]
        self.assertEqual(expect, email.to)

    def test_subscribe_email_body(self):
        email = mail.outbox[0]
        self.assertIn("Anderson Marques", email.body)
        self.assertIn("00644321229", email.body)
        self.assertIn("andersonoanjo18@mailinator.com", email.body)
        self.assertIn("984593967", email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

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


class subscribeSuccesMessage(TestCase):
    def test_message(self):
        data = dict(name="Anderson Marques", cpf="00644321229", email="andersonoanjo18@mailinator.com", phone="984593967")
        self.resp = self.client.post("/inscricao/", data, follow=True) #follow=True para seguir o redirecionamento

        self.assertContains(self.resp, "Inscrição realizada com sucesso!")
