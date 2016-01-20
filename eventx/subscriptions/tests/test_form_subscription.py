from django.test import TestCase
from eventx.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_has_fields(self):
        expect = ['name', 'cpf', 'email', 'phone']
        form = SubscriptionForm()
        self.assertSequenceEqual(expect, list(form.fields))

    def test_cpf_is_digit(self):
        """CPF must accept only digits."""
        form = self.make_validated_form(cpf="abc44321229")

        self.assertFormErrorCode(form, "cpf", "digits")

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits."""
        form = self.make_validated_form(cpf="1234")

        self.assertFormErrorCode(form, "cpf", "length")

    def test_name_must_be_capitalized(self):
        """name must be capitalized"""
        # ANDERSON marques -> Anderson Marques
        form = self.make_validated_form(name="ANDERSON marques")
        self.assertEqual("Anderson Marques", form.cleaned_data['name'])

    def test_email_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """Phone is optional"""
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """email and phone are optional but one must informed"""
        form = self.make_validated_form(phone='', email='')
        self.assertListEqual(['__all__'], list(form.errors))

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]

        self.assertEqual(code, exception.code)

    def make_validated_form(self, **kwargs):
        valid = dict(name="Anderson Marques", cpf="12345678901",
                    email="andersonoanjo18@mailinator.com", phone="984593967")
        data = dict(valid, **kwargs) #o campo que for passado no **kwargs vai atualizar o valor no dict valid
        form = SubscriptionForm(data)
        form.is_valid()

        return form