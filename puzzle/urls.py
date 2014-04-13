from django.conf.urls import patterns, url
from puzzle import views
urlpatterns = patterns('',		       
		       url(r'^submit_(?P<pk>\d+)$', views.submit, name='submit'),
		       url(r'^delete_(?P<pk>\d+)$', views.del_answer, name='delete'),
		       url(r'^puzzle(?P<pk>\d*)$', views.index, name='puzzle'),
		       url(r'^top(?P<n>\d*)$', views.toplist, name='top'),
		       )