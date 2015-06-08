from django.conf.urls import url, patterns
import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^add_category/$', views.add_category, name='add_category'),
		url(r'^category/(?P<category_enc_name>\w+)/$', views.category, name='category'),
		url(r'^add_page/(?P<category_enc_name>\w+)/$', views.add_page, name='category'),
		url(r'^register/$', views.register, name='register'),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^search/$', views.search, name='search'),
		url(r'^goto/$', views.goto_page_url, name='goto'),
		url(r'^users/$', views.view_all_users, name='users'),
		url(r'^user/(?P<username>\w+)/$', views.view_user, name='users'),
		url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
		url(r'^change_password/$', views.change_password, name='change_password'),
		url(r'^like_category/$', views.like_category, name='like_category'),
	)
