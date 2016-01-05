from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from eventx.subscriptions.forms import SubscriptionForm


def subscribe(request):
    """Essa view funciona como um dispatch(dispatch é como se fosse um roteador)"""
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, "subscription/subscription_form.html", {'form': form})

    # Send Email
    _send_mail(subject="Confirmação de inscrição",
               from_=settings.DEFAULT_FROM_EMAIL,
               to=form.cleaned_data["email"],
               template_name="subscription/subscription_email.txt",
               context=form.cleaned_data)


    # Succes feedback
    messages.success(request, "Inscrição realizada com sucesso!")

    return HttpResponseRedirect("/inscricao/")


def new(request):
    return render(request, "subscription/subscription_form.html", {'form': SubscriptionForm()})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)

    mail.send_mail(subject, body, from_, [to])
