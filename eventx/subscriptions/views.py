from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from eventx.subscriptions.forms import SubscriptionForm
from eventx.subscriptions.models import Subscription


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

    subscription = Subscription.objects.create(**form.cleaned_data)

    # Send Email
    _send_mail(subject="Confirmação de inscrição",
               from_=settings.DEFAULT_FROM_EMAIL,
               to=subscription.email,
               template_name="subscription/subscription_email.txt",
               context={'subscription': subscription})

    return HttpResponseRedirect("/inscricao/{}/".format(subscription.pk))


def new(request):
    return render(request, "subscription/subscription_form.html", {'form': SubscriptionForm()})


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, "subscription/subscription_detail.html",
                  {"subscription": subscription})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)

    mail.send_mail(subject, body, from_, [to])
