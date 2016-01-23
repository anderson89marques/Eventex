from django.shortcuts import render, get_object_or_404
from eventx.core.models import Speaker


def home(request):
    speakers = Speaker.objects.all()

    return render(request, 'index.html', context={'speakers': speakers})


def speaker_detail(request, slug):
    speaker = get_object_or_404(Speaker, slug=slug)
    return render(request, 'core/speaker_detail.html', {'speaker': speaker})