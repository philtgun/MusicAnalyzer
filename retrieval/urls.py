from django.urls import path
from . import views

urlpatterns = [
    path('search-form/', views.search_form, name='search_form'),
    path('search/', views.search, name='search'),
    path('add-track/<str:id>/', views.add_track, name='add_track'),
    path('delete-track/<str:id>/', views.delete_track, name='delete_track'),
    path('track/<str:id>/', views.track_info, name='track_info'),
]