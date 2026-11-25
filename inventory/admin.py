"""
Configuration de l'interface d'administration Django pour l'application inventory.
"""

from django.contrib import admin

from .models import Equipement


@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    """Personnalisation de l'affichage des équipements dans l'admin Django."""

    list_display = (
        "code_inventaire",
        "designation",
        "categorie",
        "marque",
        "etat",
        "salle",
        "date_acquisition",
    )
    search_fields = ("code_inventaire", "designation", "marque", "salle")
    list_filter = ("categorie", "etat", "salle")
    ordering = ("code_inventaire",)
