from django.conf.urls import url
from . import views

urlpatterns = [
				url(r'^accounts/login/$',views.login, name='login'),
				url(r'^accounts/auth/$',views.auth_view, name='auth_view'),
				url(r'^accounts/logout/$', views.logout_page, name='logout'),
				url(r'^accounts/invalid/$',views.invalid, name='invalid'),
				url(r'^accounts/register/$',views.register_user, name='register_user'),
				url(r'^accounts/register_success/$',views.register_success, name='success'),
				

				url(r'^Home/$',views.Memories_list,name='Home'),
				url(r'^Home/memory/(?P<pk>\d+)/$', views.memory_detail, name='memory_detail'),
				url(r'^Home/memory/new/$',views.new_memory,name='new_memory'),
				url(r'^Home/memory/edit/(?P<pk>\d+)/$', views.edit_memory, name='edit_memory'),
				url(r'^Home/drafts/$', views.memories_draft_list, name='memories_draft_list'),
				url(r'^Home/memory/(?P<pk>\d+)/publish/$', views.memory_publish, name='memory_publish'),
				url(r'^Home/memory/(?P<pk>\d+)/remove/$', views.memory_remove, name='memory_remove'),
				url(r'^Home/memory/(?P<pk>\d+)/public/$', views.public, name='public'),
				url(r'^Home/memory/(?P<pk>\d+)/private/$', views.private, name='private'),
				url(r'^(?P<username>\w+)/$', views.public_list, name='public_list'),
				url(r'^memory/(?P<pk>\d+)/$', views.public_detail_view, name='publicview'),
				url(r'^memory/(?P<pk>\d+)/comment/$', views.add_comment_to_memory, name='add_comment_to_memory'),
				url(r'^Home/profile/$',views.profile, name='profile'),
				url(r'^Home/profile/update/$',views.profile_update, name='profile_update'),
				url(r'^profile/?$', views.profiles, name='profiles'),
				
				]