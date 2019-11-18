from django.conf.urls import url
import form_data_app.views

urlpatterns = [
    url(r'^forms/$', form_data_app.views.FormListView.as_view(), name='data_form_list'),
    url(r'^forms/(?P<form_id>\d+)/records/$', form_data_app.views.RecordListView.as_view(), name='record_list'),
    url(r'^forms/(?P<form_id>\d+)/records/(?P<record_id>\d+)/$', form_data_app.views.RecordView.as_view(), name='record'),
]
