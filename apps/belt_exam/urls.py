from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_user$', views.add_user),
    url(r'^belt_exam$', views.belt_exam),
    url(r'^add$', views.add),
    url(r'^add_to_quotelist$', views.add_to_quotelist),
    url(r'^remove_quote$', views.remove_quote),
    url(r'quote_detail/(?P<quote_id>\d+)$', views.quote_detail),
]