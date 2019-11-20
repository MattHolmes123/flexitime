from django.urls import path

from . import views as main_views

urlpatterns = [
    path('', main_views.Index.as_view(), name='index'),
    path('this-week', main_views.ThisWeek.as_view(), name='this-week'),
    path('create/', main_views.FlexiTimeLogCreate.as_view(), name='flexitimelog_create'),
    path('update/<int:pk>', main_views.FlexiTimeLogUpdate.as_view(), name='flexitimelog_update'),
]
