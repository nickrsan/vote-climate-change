from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vote_climate.views.home', name='home'),
    # url(r'^vote_climate/', include('vote_climate.foo.urls')),

    url(r'^$', 'voteclimate.views.home'),
	url(r'^publish/$', 'voteclimate.views.add_statement'),
	url(r'^electable/find/?(?P<search_string>.+)/$', 'voteclimate.views.find_electable'),
	url(r'^electable/find/$', 'voteclimate.views.find_electable'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
