from django.urls import path

from .views import (
    # Walls
    WallListView,
    WallTagListView,
    WallDetailView,
    WallCreateView,
    WallUpdateView,
    WallDeleteView,

    # Routes
    RouteCreateView,
)


app_name = 'walls'

urlpatterns = [
    path('', WallListView.as_view(), name='list'),

    path('tag/<slug:tag>/', WallTagListView.as_view(), name='tag'),

    # Wall
    path('wall/<int:pk>/', WallDetailView.as_view(), name='detail'),
    path('wall/create/', WallCreateView.as_view(), name='create'),
    path('wall/<int:pk>/update/', WallUpdateView.as_view(), name='update'),
    path('wall/<int:pk>/delete/', WallDeleteView.as_view(), name='delete'),

    # Rotues
    path('wall/<int:pk>/add_route/', RouteCreateView.as_view(), name='add_route'),
]