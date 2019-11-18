from django.conf.urls import url
import form_design_app.views

urlpatterns = [
    url(r'^forms/$', form_design_app.views.FormListView.as_view(), name='form_list'),
    url(r'^forms/(?P<form_id>\d+)/$', form_design_app.views.FormView.as_view(), name='form'),
]
