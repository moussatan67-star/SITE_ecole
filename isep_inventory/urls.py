"""
Configuration des URLs principales du projet isep_inventory.
Inclut les routes de l'application inventory, l'interface d'administration
et la distribution des fichiers médias en mode développement.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Délégation des routes principales à l'application inventory
    path("", include("inventory.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
