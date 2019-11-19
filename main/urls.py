from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('this-week', views.this_week, name='this-week')
]
