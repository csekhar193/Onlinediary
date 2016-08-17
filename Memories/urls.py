from django.conf.urls import url
from . import views

urlpatterns = [
				url(r'^accounts/login/$',views.login),
				url(r'^accounts/auth/$',views.auth_view),
				url(r'^accounts/logout/$', views.logout_page),
				url(r'^accounts/invalid/$',views.invalid),
				url(r'^accounts/register/$',views.register_user),
				url(r'^accounts/register_success/$',views.register_success),
				url(r'^Home/$',views.Memories_list,name='Memories_list'),
				url(r'^Home/memory/(?P<pk>\d+)/$', views.memory_detail, name='memory_detail'),
				url(r'^Home/memory/new/$',views.new_memory,name='new_memory'),
				url(r'^Home/memory/(?P<pk>\d+)/edit/$', views.edit_memory, name='edit_memory'),
				url(r'^Home/drafts/$', views.memories_draft_list, name='memories_draft_list'),
				url(r'^Home/memory/(?P<pk>\d+)/publish/$', views.memory_publish, name='memory_publish'),
				url(r'^Home/memory/(?P<pk>\d+)/remove/$', views.memory_remove, name='memory_remove'),
				]