from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.index, name='index'),
    url(r'^sign/$', views.sign_in, name='sign'),
    url(r'^thankyou/$', views.thankyou, name=''),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/register/$', views.register, name='register'),
    url(r'^(?P<user_name>\w+)/$',views.load_profile, name='load_profile'),
    url(r'^(?P<hospital_name>\w+)/(?P<doctor_user_name>\w+)/pool/$',views.patient_pool,name='patient_pool'),
    url(r'^(?P<hospital_name>\w+)/(?P<doctor_user_name>\w+)/pool/(?P<user_name>\w+)/save/$',views.patien_to_save, name='patient_to_save'),
    url(r'^(?P<user_name>\w+)/send/$',views.send_message,name='send'),
    url(r'^(?P<hospital_name>\w+)/sign/$',views.doctor_sign,name='doctor_sign'),
    url(r'^(?P<hospital_name>\w+)/sign/doctor/',views.doctor_verify,name="doctor_verify"),
    url(r'^(?P<doctor_user_name>\w+)/doctor/profie',views.doctor_profile,name='doctor_profile'),


]
