from django.core import mail
from django.test import TestCase
from eventx.subscriptions.forms import SubscriptionForm


class SubscribeGet(TestCase):
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


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Anderson Marques", cpf="00644321229", email="andersonoanjo18@mailinator.com", phone="984593967")
        self.resp = self.client.post("/inscricao/", data)

    def test_redirect_post(self):
        """ Após a requisição o usuário deve ser redirecionado para inscricao/ """

        self.assertEqual(302, self.resp.status_code)

    def test_send_email(self):
        """ Deve ser enviando um email de confirmação de inscricao """

        self.assertEqual(1, len(mail.outbox))

class SubscribePostInvalid(TestCase):
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
