from django import forms
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError("Cpf deve conter apenas números!", 'digits')

    if len(value) < 11:
        raise ValidationError("Cpf deve ter 11 digitos!", 'length')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome:')
    cpf = forms.CharField(label='Cpf:', validators=[validate_cpf, ])
    email = forms.EmailField(label='Email:')
    phone = forms.CharField(label='Telefone:')

    def clean_name(self): #o django procurar por clean_nomeDoAtributo
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]

        #É sempre preciso retorna alguma coisa
        return ' '.join(words)