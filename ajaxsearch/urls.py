from django.conf.urls.defaults import *
from ajaxsearch.views import *
from django.conf.urls import url
from django.contrib import admin
from pages import views as page_views

urlpatterns = [ '',
         url( r'^$', index, name = 'demo_index' ),
         url( r'^users/$', ajax_user_search, name = 'demo_user_search' ),
                              ]

                              