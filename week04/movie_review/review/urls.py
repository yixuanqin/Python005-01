from django.urls import path
from . import views

urlpatterns = [
    path('', views.default),
    path('search', views.search, name = 'search'),
]


