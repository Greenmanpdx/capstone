"""capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from pages import views as page_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', page_views.home, name='home'),
    url(r'^encounters/(?P<pk>[\w]+)', page_views.encounter_builder, name='encounter_builder'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^search_api/', page_views.search_api, name='search_api'),
    url(r'^add_monster_api/', page_views.add_monster_api, name='add_monster_api'),
    url(r'^create_encounter/', page_views.create_encounter, name='create_encounter'),
    url(r'^create_player/', page_views.create_player, name='create_player'),
    url(r'^create_session/', page_views.create_session, name='create_session'),
    url(r'^player_to_session/', page_views.player_to_session, name='player_to_session'),
    url(r'^encounter_to_session/', page_views.encounter_to_session, name='encounter_to_session'),
    url(r'^set_session/', page_views.set_session, name='set_session'),
    url(r'^combat/(?P<pk>[\w]+)', page_views.combat, name='combat'),
    url(r'^initiative_tracker', page_views.initiative_tracker, name='initiative_tracker')

]
