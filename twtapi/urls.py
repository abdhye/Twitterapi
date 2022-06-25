from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),

    path('twitter', views.twitter, name='goto-twitter'),
    path('twitter', views.twitter, name='twitter'),
    path('twitter/search', views.search_twt, name='search-twt'),

    path('marvel', views.marvel, name='marvel'),
    path('marvel', views.marvel, name='goto-marvel-coverpage'),
    path('marvel/characters', views.mar_chars, name='goto-mar-charpage'),
    path('marvel/comics', views.mar_comics, name='goto-mar-comicspage'),
]
