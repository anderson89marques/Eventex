from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string
from eventx.subscriptions.forms import SubscriptionForm
from eventx.subscriptions.models import Subscription


def new(request):
    """Essa view funciona como um dispatch(dispatch é como se fosse um roteador)"""

    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    return render(request, "subscription/subscription_form.html", {'form': SubscriptionForm()})


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, "subscription/subscription_form.html", {'form': form})

    subscription = form.save() #uso quando o formulário é muito alinhado com o modelo.
    #subscription = Subscription.objects.create(**form.cleaned_data)

    # Send Email
    _send_mail(subject="Confirmação de inscrição",
               from_=settings.DEFAULT_FROM_EMAIL,
               to=subscription.email,
               template_name="subscription/subscription_email.txt",
               context={'subscription': subscription})

    return HttpResponseRedirect(r("subscription:detail", subscription.pk))


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
