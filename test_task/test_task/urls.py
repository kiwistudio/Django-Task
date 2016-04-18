from django.conf.urls import include, url
from django.contrib import admin
from myauth.views import UserDelete, UserUpdate

urlpatterns = [
    
    url(r'^$', 'myauth.views.user_list', name='home'),
	url(r'^user/add/$', 'myauth.views.user_add', name='user_add'),
	url(r'^user/(?P<pk>\d+)/edit/$', UserUpdate.as_view(), name='user_edit'),
	url(r'^user/(?P<pk>\d+)/delete/$', UserDelete.as_view(), name='user_delete'),
	url(r'^export$', 'myauth.views.export_excel', name='export'),
    url(r'^admin/', include(admin.site.urls)),
]
