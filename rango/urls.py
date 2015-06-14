from django.conf.urls import url, patterns
import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^add_category/$', views.add_category, name='add_category'),
		url(r'^category/(?P<category_enc_name>\w+)/$', views.category, name='category'),
		url(r'^add_page/(?P<category_enc_name>\w+)/$', views.add_page, name='add_page'),
		url(r'^register/$', views.register, name='register'),
		url(r'^login/$', views.user_login, name='user_login'),
		url(r'^logout/$', views.user_logout, name='user_logout'),
		url(r'^search/$', views.search, name='search'),
		url(r'^goto/$', views.goto_page_url, name='goto_page_url'),
		url(r'^users/$', views.view_all_users, name='view_all_users'),
		url(r'^user/(?P<username>\w+)/$', views.view_user, name='view_user'),
		url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
		url(r'^change_password/$', views.change_password, name='change_password'),
		url(r'^like_category/$', views.like_category, name='like_category'),
	)
