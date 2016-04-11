from django.conf.urls import url, include
import views


urlpatterns = [
    url(r'^$', views.get_index_page),
    url(r'^search/twitter/timeline/(?P<handler>([aA-zZ]+))/$', views.TimeLineView.as_view()),
    url(r'^search/twitter/most-used-hashtags/(?P<handler>([aA-zZ]+))/$', views.MostUsedHashTag.as_view()),
    url(r'^search/twitter/favourite-tweets/(?P<handler>([aA-zZ]+))/$', views.FavouriteTweets.as_view()),
]
