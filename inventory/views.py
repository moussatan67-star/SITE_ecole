"""
Vues basées sur des fonctions pour la gestion du parc informatique ISEP.
Fournit le tableau de bord, le CRUD complet des équipements, la recherche et le filtrage.
"""

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EquipementForm
from .models import Equipement


def home(request):
    """Redirige la page d'accueil vers le tableau de bord."""
    return redirect("inventory:dashboard")


def dashboard(request):
    """Affiche les statistiques globales du parc et les 5 derniers équipements ajoutés."""
    total_equipements = Equipement.objects.count()
    nb_disponibles = Equipement.objects.filter(
        etat=Equipement.Etat.DISPONIBLE
    ).count()
    nb_en_panne = Equipement.objects.filter(
        etat=Equipement.Etat.EN_PANNE
    ).count()
    nb_en_maintenance = Equipement.objects.filter(
        etat=Equipement.Etat.EN_MAINTENANCE
    ).count()
    derniers_equipements = Equipement.objects.order_by("-id")[:5]

    context = {
        "total_equipements": total_equipements,
        "nb_disponibles": nb_disponibles,
        "nb_en_panne": nb_en_panne,
        "nb_en_maintenance": nb_en_maintenance,
        "derniers_equipements": derniers_equipements,
    }
    return render(request, "inventory/dashboard.html", context)


def equipement_list(request):
    """Liste les équipements avec recherche (désignation ou code) et filtres combinables."""
    equipements = Equipement.objects.all()

    q = request.GET.get("q", "").strip()
    categorie = request.GET.get("categorie", "").strip()
    etat = request.GET.get("etat", "").strip()

    if q:
        equipements = equipements.filter(
            Q(designation__icontains=q) | Q(code_inventaire__icontains=q)
        )

    if categorie:
        equipements = equipements.filter(categorie=categorie)

    if etat:
        equipements = equipements.filter(etat=etat)

    context = {
        "equipements": equipements,
        "q": q,
        "categorie_selected": categorie,
        "etat_selected": etat,
        "categories": Equipement.Categorie.choices,
        "etats": Equipement.Etat.choices,
        "filtres_actifs": bool(q or categorie or etat),
    }
    return render(request, "inventory/equipement_list.html", context)


def equipement_detail(request, pk):
    """Affiche la fiche détaillée d'un équipement."""
    equipement = get_object_or_404(Equipement, pk=pk)
    return render(
        request,
        "inventory/equipement_detail.html",
        {"equipement": equipement},
    )


def equipement_create(request):
    """Crée un nouvel équipement à partir du formulaire EquipementForm."""
    if request.method == "POST":
        form = EquipementForm(request.POST, request.FILES)
        if form.is_valid():
            equipement = form.save()
            messages.success(
                request,
                f"L'équipement « {equipement} » a été ajouté avec succès.",
            )
            return redirect("inventory:equipement_list")
    else:
        form = EquipementForm()

    context = {
        "form": form,
        "titre": "Ajouter un équipement",
        "bouton_label": "Enregistrer",
        "is_edit": False,
    }
    return render(request, "inventory/equipement_form.html", context)


def equipement_update(request, pk):
    """Modifie un équipement existant."""
    equipement = get_object_or_404(Equipement, pk=pk)

    if request.method == "POST":
        form = EquipementForm(request.POST, request.FILES, instance=equipement)
        if form.is_valid():
            equipement = form.save()
            messages.success(
                request,
                f"L'équipement « {equipement} » a été mis à jour.",
            )
            return redirect("inventory:equipement_list")
    else:
        form = EquipementForm(instance=equipement)

    context = {
        "form": form,
        "equipement": equipement,
        "titre": f"Modifier « {equipement.code_inventaire} »",
        "bouton_label": "Mettre à jour",
        "is_edit": True,
    }
    return render(request, "inventory/equipement_form.html", context)


def equipement_delete(request, pk):
    """Affiche la page de confirmation (GET) puis supprime l'équipement (POST)."""
    equipement = get_object_or_404(Equipement, pk=pk)

    if request.method == "POST":
        libelle = str(equipement)
        equipement.delete()
        messages.success(
            request,
            f"L'équipement « {libelle} » a été supprimé de l'inventaire.",
        )
        return redirect("inventory:equipement_list")

    return render(
        request,
        "inventory/equipement_confirm_delete.html",
        {"equipement": equipement},
    )
