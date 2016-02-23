from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.index, name='index'),
    url(r'^sign/$', views.sign_in, name='sign'),
    url(r'^thankyou/$', views.thankyou, name='thankyou'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/register/$', views.register, name='register')

]
