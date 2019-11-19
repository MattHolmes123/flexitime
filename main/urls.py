from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('this-week', views.this_week, name='this-week'),
    path('edit-today/<int: pk>', views.edit_today, name='edit-today')
]
