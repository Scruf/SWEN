from django.conf.urls import url,patterns,include
from . import views

urlpatterns =[
    url(r'^$', views.index, name='index'),
    #api
    url(r'^api/users/$',views.patient,name='patient'),
    url(r'^api/apoitment(?P<apoitment_time>\w+)/$',views.check_for_time,name='check_for_time'),
    #end of apis
    url(r'^administration/$', views.administration,name='administration'),
    url(r'^administration/(?P<admin_name>\w+)/create/$',views.admin_create,name='admin_create'),
    url(r'^administration/admin/$', views.admin_verify,name='admin_verify'),
    url(r'^administration/(?P<admin_name>\w+)/$',views.admin_profile,name='admin_profile'),
    url(r'^administration/(?P<admin_name>\w+)/create/verify/$',views.admin_create_verify,name='admin_create_verify'),
    url(r'^administration/(?P<admin_name>\w+)/logs$',views.admin_logs,name='admin_logs'),

    # url(r'^administration/register/$',views.administration_save,name='administration_save'),
    #message url
    url(r'^(?P<sender_name>\w+)/message/$',views.message,name='message'),
    #end of message url
    url(r'^sign/$', views.sign_in, name='sign'),
    url(r'^thankyou/$', views.thankyou, name=''),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/register/$', views.register, name='register'),
    url(r'^(?P<user_name>\w+)/$',views.load_profile, name='load_profile'),
    url(r'^(?P<user_name>\w+)/view/$', views.profile_edit,name='view_profile'),
    url(r'^(?P<user_name>\w+)/view/save/$', views.save_profile,name='save_profile'),
    url(r'^(?P<user_name>\w+)/appoitment/$',views.appoitment,name='appoitment'),
    url(r'^(?P<user_name>\w+)/appoitment/view/$',views.edit_apoitment,name='edit_apoitment'),
    url(r'^(?P<user_name>\w+)/appoitment/view/details/(?P<title>\w+)/(?P<date_url>\w+)/$',views.view_appoitment,name='view_appoitment'),
    url(r'^(?P<user_name>\w+)/appoitment/edit/(?P<apoitment_id>[0-9]+)/$',views.edit_apoitment_,name='edit_apoitment_'),
    url(r'^appoitment/edit/(?P<apoitment_id>[0-9]+)/save/$',views.apoitment_save, name='apoitment_save'),
    url(r'^(?P<user_name>\w+)/appoitment/confirm/$',views.confirm_appoitment,name='confirm_appoitment'),
    url(r'^(?P<user_name>\w+)/appoitment/confirm/(?P<dates>[\w|\W]+)/$',views.confirm_appoitment_dates,name='confirm_appoitment_dates'),
    url(r'^(?P<hospital_name>\w+)/(?P<doctor_user_name>\w+)/pool/$',views.patient_pool,name='patient_pool'),
    url(r'^(?P<hospital_name>\w+)/(?P<doctor_user_name>\w+)/pool/(?P<patient_uesr_name>\w+)/view$',views.patient_pool_view,name='patient_pool'),
    url(r'^(?P<hospital_name>\w+)/(?P<doctor_user_name>\w+)/pool/(?P<user_name>\w+)/save/$',views.patien_to_save, name='patient_to_save'),
    #urls for doctors go bellow
    url(r'^doctor/(?P<doctor_user_name>\w+)/$',views.doctor_profile,name='doctor_profile'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/edit/$',views.doctor_edit_profile,name='doctor_edit_profile'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/edit/doctor_edit/$',views.doctor_edit_profile_save,name='doctor_edit_profile_save'),

    #urls for doctors go above
]
