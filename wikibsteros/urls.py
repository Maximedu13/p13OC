# -*- coding: utf-8 -*-
""" wikibsteros app urls """
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'wikibsteros'

urlpatterns = [
    path('', views.index, name='index'),
    path('wikibsteros', views.wikibsteros, name='wikibsteros'),
    path('universe', views.universe, name='universe'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('log_out', views.log_out, name='logout'),
    path('universe/battle', views.battle, name='battle'),
    path('universe/test', views.test_i18n, name='test'),
    path('universe/weather', views.weather, name='weather'),
    path('wikibsteros/character/<str:id>', views.character, name='character'),
    path('wikibsteros/house/<str:id>', views.house, name='house'),
    path('wikibsteros/city/<str:id>', views.city, name='city'),
    path('wikibsteros/articles/', views.articles, name='articles'),
    path('wikibsteros/article/<str:id>', views.article, name='article'),
    path('universe/battle_result', views.battle_result, name='battle_result'),
    path('universe/maggy', views.maggy, name='maggy'),
    path('wikibsteros/search', views.wikibsteros_search, name='wikibsteros_search'),
    path('wikibsteros/add_comment_city/<str:city_id>', views.add_a_comment_city, name='add_a_comment_city'),
    path('wikibsteros/add_comment_character/<str:character_id>', views.add_a_comment_character, name='add_a_comment_character'),
    path('wikibsteros/add_comment_article/<str:article_id>', views.add_a_comment_article, name='add_a_comment_article'),
    path('wikibsteros/add_a_vote/<str:char_id>', views.add_a_vote_character, name='add_a_vote'),
]
