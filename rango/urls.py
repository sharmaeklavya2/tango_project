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
	)
