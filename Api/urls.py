from django.conf.urls import url, include
from django.contrib import admin
from Api import views
urlpatterns = [

    # for our home/index page


    # when short URL is requested it redirects to original URL
url(r'^long-url/$', views.Longer.as_view(), name='longurl'),
url(r'^long-urls/$', views.LongerList.as_view(), name='longurls'),
    url(r'^short-url/$', views.Shorten.as_view(), name='shortenurl'),
url(r'^short-urls/$', views.ShortenList.as_view(), name='shorturls'),
url(r'^count/$', views.Count.as_view(), name='count'),
]
