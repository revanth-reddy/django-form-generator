from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/design/', include('form_design_app.urls')),
    url(r'^api/data/', include('form_data_app.urls')),
]
