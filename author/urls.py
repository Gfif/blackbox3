from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from author import views


def author_required(function=None, login_url=None):
    actual_decorator = permission_required('game.add_task',
                                           login_url=login_url)
    if function is None:
        return actual_decorator(login_required)
    return actual_decorator(login_required(function))


urlpatterns = patterns(
    '',

    url(r'^$', RedirectView.as_view(url=reverse_lazy('author-login'),
                                    permanent=False)),

    url(r'^login/$',
        login,
        {'template_name': 'author/login.html'},
        name='author-login'),

    url(r'^logout/$',
        logout,
        {'next_page': reverse_lazy('author-login')},
        name='author-logout'),

    url(r'^panel/$',
        author_required(function=views.PanelView.as_view(),
                        login_url=reverse_lazy('author-login')),
        name='panel'),
)
