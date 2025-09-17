from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health_check, name="health"),
    path("floodcontrol/", views.get_floodcontrol, name="get_floodcontrol"),
    path("floodcontrol/create/", views.create_floodcontrol, name="create_floodcontrol"),
    path("floodcontrol/<int:id>/", views.get_floodcontrol_item, name="get_floodcontrol_item"),
    path("floodcontrol/<int:id>/update/", views.update_floodcontrol, name="update_floodcontrol"),
    path("floodcontrol/<int:id>/delete/", views.delete_floodcontrol, name="delete_floodcontrol"),
    path("", views.index, name="index"),
]
