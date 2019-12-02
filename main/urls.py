from django.urls import path

from . import views as main_views

urlpatterns = [
    path('', main_views.Index.as_view(), name='index'),
    path('this_week', main_views.ThisWeek.as_view(), name='this_week'),
    path('edit_today', main_views.edit_today, name='edit_today'),
    path('edit_week', main_views.edit_week, name='edit_week'),
    path('create/', main_views.FlexiTimeLogCreateView.as_view(), name='create'),
    path('update/<int:pk>', main_views.FlexiTimeLogUpdateView.as_view(), name='update'),
    path('detail/<int:pk>', main_views.FlexiTimeLogDetailView.as_view(), name='detail')
]
