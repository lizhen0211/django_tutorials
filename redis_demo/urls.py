from django.conf.urls import url

from redis_demo.views import SetDjangoRedisCacheView, GetDjangoRedisCacheView, SetCacheView, SetCacheParamView, \
    SetCacheListView, SetCacheSetView, HashView, GroupByKeyView

urlpatterns = [
    url(r'^redis/set_cache$', SetDjangoRedisCacheView.as_view()),
    url(r'^redis/get_cache$', GetDjangoRedisCacheView.as_view()),
    url(r'^redis/native_set_cache$', SetCacheView.as_view()),
    url(r'^redis/native_set_cache_param$', SetCacheParamView.as_view()),
    url(r'^redis/native_hash$', HashView.as_view()),
    url(r'^redis/native_set_cache_list$', SetCacheListView.as_view()),
    url(r'^redis/native_set_cache_group_by_key$', GroupByKeyView.as_view()),
    url(r'^redis/native_set_cache_set$', SetCacheSetView.as_view()),

]
