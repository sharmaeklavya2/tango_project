from django.conf.urls import url, patterns
import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^category/(?P<category_enc_name>\w+)/$', views.category, name='category'),
		url(r'^add_category/$', views.add_category, name='add_category'),
	)
