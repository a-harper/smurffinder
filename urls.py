from django.conf.urls import url

from . import views

urlpatterns = [
    # e.g. /smurf/
    url(r'^$', views.index, name='index'),
    # e.g. /smurf/proxy/
    url(r'^proxy/$', views.smurfproxy, name='smurfproxy'),
    # e.g. /smurf/[steamid]/
    url(r'^(?P<steamid>[^/]+)$', views.smurflist, name='smurflist'),
    # e.g. /smurf/steamid1,steamid2/
    url(r'(?P<steamid_smurf>[^/]+)/(?P<steamid_friend>[^/]+)', views.smurfproxylist, name='smurfproxylist')
    # url(r'(?P<username>[^/]+)/r/(?P<subreddit>[^/]+)', views.subreddits, name='subreddits'),
]
