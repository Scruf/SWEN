from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.index, name='index'),
    url(r'^sign/$', views.sign_in, name='sign'),

]
