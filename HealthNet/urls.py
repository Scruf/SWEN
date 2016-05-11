from django.conf.urls import url,patterns,include
from . import views

urlpatterns =[
    url(r'^$', views.index, name='index'),
    #api
    url(r'^api/users/$',views.patient,name='patient'),
    # url(r'^api/(?P<sender_name>\w+)/(?P<hospital_name>\w+)/message/$',views.message,name='message'),

    #will return the available time for a doctor
    url(r'^api/apoitment/(?P<doctor_name>\w+)/(?P<apoitment_date>\w+)/$',views.check_fo_time,name='check_for_time'),
    url(r'^api/doctor_names/(?P<doctor_name>\w+)/$', views.doctor_names,name='doctor_names'),
    url(r'^api/appoitment/submit/$',views.apoitment_submit,name='apoitment_submit'),
    #end of apis
    url(r'^administration/$', views.administration,name='administration'),
    url(r'^administration/(?P<admin_name>\w+)/create/$',views.admin_create,name='admin_create'),
    url(r'^administration/admin/$', views.admin_verify,name='admin_verify'),
    url(r'^administration/(?P<admin_name>\w+)/$',views.admin_profile,name='admin_profile'),
    url(r'^administration/(?P<admin_name>\w+)/create/verify/$',views.admin_create_verify,name='admin_create_verify'),
    url(r'^administration/(?P<admin_name>\w+)/logs$',views.admin_logs,name='admin_logs'),
    url(r'^administration/(?P<admin_name>\w+)/stats/$',views.statistics,name='advanced_statistics'),
    #url for apoitment modifications
    url(r'^(?P<user_name>\w+)/(?P<doctor_name>\w+)/(?P<apoitment_id>[0-9]+)/appoitment/views/$',views.apoitment_view,name='apoitment_view'),
    url(r'^(?P<user_name>\w+)/(?P<doctor_name>\w+)/(?P<apoitment_id>[0-9]+)/appoitment/views/edit/$',views.apoitment_view_edit,name='apoitment_view_edit'),
    url(r'^(?P<user_name>\w+)/(?P<doctor_name>\w+)/(?P<apoitment_id>[0-9]+)/appoitment/views/delete/$',views.apoitment_view_edit_delete,name='apoitment_view_edit_delete'),
    url(r'^(?P<user_name>\w+)/(?P<doctor_name>\w+)/(?P<apoitment_id>[0-9]+)/appoitment/views/edit/submit/$',views.apoitment_view_edit_submit,name='apoitment_view_edit_submit'),
    url(r'^doctor/(?P<doctor_name>\w+)/(?P<user_name>\w+)/(?P<apoitment_id>[0-9]+)/appoitment/view/$',views.doctor_apoitment_view,name='doctor_apoitment_view'),
    url(r'^doctor/(?P<doctor_name>\w+)/(?P<user_name>\w+)/(?P<apoitment_id>[0-9]+)/appoitment/view/edit/$',views.doctor_apoitment_view_edit,name='doctor_apoitment_view_edit'),
    url(r'^doctor/(?P<doctor_name>\w+)/(?P<user_name>\w+)/(?P<apoitment_id>[0-9]+)/appoitment/view/edit/submit/$',views.doctor_apoitment_view_edit_submit,name='doctor_apoitment_view_edit_submit'),
    url(r'^doctor/(?P<doctor_name>\w+)/(?P<user_name>\w+)/(?P<apoitment_id>[0-9]+)/appoitment/view/delete/$',views.doctor_apoitment_view_delete,name='doctor_apoitment_view_delete'),
    #end of appoitment modifications
    # url(r'^administration/register/$',views.administration_save,name='administration_save'),
    #message url
    url(r'^(?P<sender_name>\w+)/message/$',views.message,name='message'),
    url(r'^(?P<sender_name>\w+)/message/send/$',views.message_send_view,name='message'),
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


    # url(r'^(?P<user_name>\w+)/appoitment/confirm/$',views.confirm_appoitment,name='confirm_appoitment'),
    url(r'^(?P<user_name>\w+)/appoitment/confirm/(?P<dates>[\w|\W]+)/$',views.confirm_appoitment_dates,name='confirm_appoitment_dates'),
    url(r'^(?P<hospital_name>\w+)/(?P<doctor_user_name>\w+)/pool/$',views.patient_pool,name='patient_pool'),
    url(r'^(?P<hospital_name>\w+)/(?P<doctor_user_name>\w+)/pool/(?P<patient_uesr_name>\w+)/view$',views.patient_pool_view,name='patient_pool'),
    url(r'^(?P<hospital_name>\w+)/(?P<doctor_user_name>\w+)/pool/(?P<user_name>\w+)/save/$',views.patien_to_save, name='patient_to_save'),
    #urls for doctors go bellow
    url(r'^doctor/(?P<doctor_user_name>\w+)/$',views.doctor_profile,name='doctor_profile'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/edit/$',views.doctor_edit_profile,name='doctor_edit_profile'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/edit/doctor_edit/$',views.doctor_edit_profile_save,name='doctor_edit_profile_save'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/patients/$',views.patients,name='doctor_patients'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/patients/(?P<patient_uesr_name>\w+)/add/$',views.loadaddprescription,name='doctor_add_prescription'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/patients/(?P<patient_uesr_name>\w+)/add/confirm/$',views.addPrescription,name='addPrescription'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/patients/(?P<patient_uesr_name>\w+)/viewprescriptions/$',views.viewPrescriptions,name='viewprescriptions'),
    url(r'^doctor/(?P<doctor_user_name>\w+)/patients/(?P<patient_uesr_name>\w+)/viewprescriptions/(?P<medicine_id>[0-9]+)/$',views.deletePrescription,name='deleteprescription'),
    #urls for doctors go above

    #nurses
    url(r'^nurse/(?P<nurse_user_name>\w+)/$',views.nurse_profile,name='nurse_profile'),
    url(r'^nurse/(?P<nurse_user_name>\w+)/edit/$',views.nurse_edit_profile,name='nurse_edit_profile'),
    url(r'^nurse/(?P<nurse_user_name>\w+)/edit/nurse_edit/$',views.nurse_edit_profile_save,name='nurse_edit_profile_save')

]
