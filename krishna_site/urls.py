from django.contrib import admin
from django.urls import path
from main import views


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        views.home
    ),

    path(
        'transition/',
        views.transition,
        name='transition'
    ),

    path(
        'welcome/',
        views.welcome,
        name='welcome'
    ),

    path(
        'game/',
        views.game,
        name='game'
    ),

    path(
        'makhan/',
        views.makhan,
        name='makhan'
    ),

    path(
        'memory/',
        views.memory,
        name='memory'
    ),

    path(
        'explore/',
        views.explore,
        name='explore'
    ),

    path(
        'explore-api/',
        views.explore_api,
        name='explore_api'
    ),

]
path(
    'download-photo/',
    views.download_photo,
    name='download_photo'
),