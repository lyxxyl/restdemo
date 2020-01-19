"""restdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^books/$',views.BookViewSet.as_view(),name='book_list'),
    # url(r'^books/(?P<pk>\d+)/$', views.BookDetailViewSet.as_view(), name='book_detail'),
    url(r'^books/$',views.BookViewSet.as_view({"get":"list","post":"create"}),name='book_list'),
    url(r'^books/(?P<pk>\d+)/$', views.BookViewSet.as_view({'get':'retrieve',
                                                                  'put':'update',
                                                                  'delete':'destroy'}), name='book_detail'),
    url(r'^publishers/$', views.PublishViewSet.as_view(), name='publish_list'),
    url(r'^publishers/(?P<pk>\d+)/$', views.PublishDetailViewSet.as_view(), name='publish_detail'),

    url(r'^authors/$', views.AuthorViewSet.as_view(), name='author_list'),
    url(r'^authors/(\d+)/$', views.AuthorDetailViewSet.as_view(), name='author_detail'),
    url(r'^login/$', views.LoginViewSet.as_view(), name='login'),

]
