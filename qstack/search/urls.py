from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^$', 'search.views.home', name='home'),
                       url(r'^process-search/$',
                           'search.views.process_search',
                           name='process_search'), )
