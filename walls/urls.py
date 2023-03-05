from django.urls import path

from .views import (
    # Walls
    WallListView,
    WallTagListView,
    WallDetailView,
    WallCreateView,
    create_wall,
    WallUpdateView,
    WallDeleteView,
    add_wall_holds,

    # Routes
    create_route,
    route_detail
)


app_name = 'walls'

urlpatterns = [
    path('walls', WallListView.as_view(), name='list'),

    path('tag/<slug:tag>/', WallTagListView.as_view(), name='tag'),

    # Wall
    path('walls/<int:pk>/', WallDetailView.as_view(), name='detail'),
    path('walls/create/', create_wall, name='create'),
    path('walls/<int:pk>/add_holds/', add_wall_holds, name='add_holds'),
    path('walls/<int:pk>/update/', WallUpdateView.as_view(), name='update'),
    path('walls/<int:pk>/delete/', WallDeleteView.as_view(), name='delete'),

    # Rotues
    path('walls/<int:pk>/add_route/', create_route, name='add_route'),
    path('walls/<int:pk>/route/<int:route_pk>', route_detail, name='route_detail'),
]