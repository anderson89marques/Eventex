import os
from django.core.urlresolvers import get_urlconf, set_urlconf, resolve, reverse
from django.conf.urls import url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventx.settings')


def index(request): pass
def auth(request): pass


class MySiteUrlConf:
    urlpatterns = [
        url(r'^$', index, name='index'),
        url(r'^login/$', auth, kwargs={'action': 'login'}, name='login'),
        url(r'^logout/$', auth, kwargs={'action': 'logout'}, name='logout'),
    ]

set_urlconf(MySiteUrlConf)
print()
print("Resolve:", resolve('/'))
print("Resolve:", resolve('/login/'))
print("Resolve:", resolve('/logout/'))

print()
print("Reverse:", reverse('index'))
print("Reverse:", reverse('login'))
print("Reverse:", reverse('logout'))