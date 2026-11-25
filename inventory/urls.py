"""
Définition des routes de l'application inventory.
"""

from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("equipements/", views.equipement_list, name="equipement_list"),
    path("equipements/ajouter/", views.equipement_create, name="equipement_create"),
    path("equipements/<int:pk>/", views.equipement_detail, name="equipement_detail"),
    path(
        "equipements/<int:pk>/modifier/",
        views.equipement_update,
        name="equipement_update",
    ),
    path(
        "equipements/<int:pk>/supprimer/",
        views.equipement_delete,
        name="equipement_delete",
    ),
]
