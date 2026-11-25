"""
Tests unitaires et fonctionnels de l'application inventory.
Exécution : python manage.py test
"""

from datetime import date
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from .models import Equipement


class EquipementInventoryTests(TestCase):
    """Vérifie le modèle, le CRUD complet, la recherche, le filtrage et le dashboard."""

    def setUp(self):
        self.eq_dispo = Equipement.objects.create(
            code_inventaire="INV-001",
            designation="Dell Latitude 5540",
            categorie=Equipement.Categorie.ORDINATEUR,
            marque="Dell",
            numero_serie="SN-DL5540-01",
            date_acquisition=date(2024, 3, 15),
            etat=Equipement.Etat.DISPONIBLE,
            salle="Labo Info",
            observations="16 Go RAM, SSD 512 Go.",
        )
        self.eq_panne = Equipement.objects.create(
            code_inventaire="INV-002",
            designation="Canon i-SENSYS MF453dw",
            categorie=Equipement.Categorie.IMPRIMANTE,
            marque="Canon",
            date_acquisition=date(2023, 6, 10),
            etat=Equipement.Etat.EN_PANNE,
            salle="Bureau Direction",
        )
        self.eq_maint = Equipement.objects.create(
            code_inventaire="INV-003",
            designation="Epson EB-X51",
            categorie=Equipement.Categorie.VIDEOPROJECTEUR,
            marque="Epson",
            date_acquisition=date(2023, 9, 5),
            etat=Equipement.Etat.EN_MAINTENANCE,
            salle="Salle 101",
        )

    def test_redirection_accueil_vers_dashboard(self):
        """La racine / redirige vers /dashboard/."""
        response = self.client.get(reverse("inventory:home"))
        self.assertRedirects(response, reverse("inventory:dashboard"))

    def test_ajout_equipement(self):
        """L'ajout d'un équipement valide crée l'objet et redirige vers la liste."""
        donnees = {
            "code_inventaire": "INV-010",
            "designation": "Switch Cisco 2960",
            "categorie": Equipement.Categorie.RESEAU,
            "marque": "Cisco",
            "date_acquisition": "2024-05-20",
            "etat": Equipement.Etat.DISPONIBLE,
            "salle": "Baie Réseau",
        }
        response = self.client.post(
            reverse("inventory:equipement_create"),
            data=donnees,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Equipement.objects.filter(code_inventaire="INV-010").exists()
        )
        self.assertContains(response, "Switch Cisco 2960")

    def test_affichage_liste(self):
        """La vue liste retourne 200 et affiche les équipements existants."""
        response = self.client.get(reverse("inventory:equipement_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "INV-001")
        self.assertContains(response, "INV-002")
        self.assertContains(response, "INV-003")

    def test_page_detail(self):
        """La page détail affiche toutes les informations et l'image par défaut."""
        response = self.client.get(
            reverse("inventory:equipement_detail", args=[self.eq_dispo.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"#{self.eq_dispo.pk}")
        self.assertContains(response, "Dell Latitude 5540")
        self.assertContains(response, "Labo Info")
        self.assertContains(response, "SN-DL5540-01")
        self.assertContains(response, "16 Go RAM, SSD 512 Go.")
        self.assertContains(response, "inventory/img/ordinateur.svg")

    def test_upload_image_affiche_sur_detail(self):
        """Une image téléversée lors de l'ajout est affichée sur la fiche détail."""
        buffer = BytesIO()
        Image.new("RGB", (40, 40), color=(0, 153, 255)).save(buffer, format="PNG")
        image_file = SimpleUploadedFile(
            "test_pc.png",
            buffer.getvalue(),
            content_type="image/png",
        )
        response = self.client.post(
            reverse("inventory:equipement_create"),
            data={
                "code_inventaire": "INV-099",
                "designation": "PC Image Test",
                "categorie": Equipement.Categorie.ORDINATEUR,
                "marque": "Dell",
                "date_acquisition": "2024-06-01",
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Labo Info",
                "image": image_file,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        equipement = Equipement.objects.get(code_inventaire="INV-099")
        self.assertTrue(bool(equipement.image))

        detail_res = self.client.get(
            reverse("inventory:equipement_detail", args=[equipement.pk])
        )
        self.assertContains(detail_res, equipement.image.url)
        equipement.image.delete(save=False)

    def test_modification_etat(self):
        """La modification met à jour l'état de l'équipement en base."""
        donnees = {
            "code_inventaire": self.eq_panne.code_inventaire,
            "designation": self.eq_panne.designation,
            "categorie": self.eq_panne.categorie,
            "marque": self.eq_panne.marque,
            "date_acquisition": "2023-06-10",
            "etat": Equipement.Etat.DISPONIBLE,
            "salle": self.eq_panne.salle,
        }
        response = self.client.post(
            reverse("inventory:equipement_update", args=[self.eq_panne.pk]),
            data=donnees,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.eq_panne.refresh_from_db()
        self.assertEqual(self.eq_panne.etat, Equipement.Etat.DISPONIBLE)

    def test_mise_a_jour_statistiques_dashboard(self):
        """Les compteurs du dashboard reflètent les ajouts, modifications et suppressions."""
        url_dashboard = reverse("inventory:dashboard")

        # État initial : 3 équipements (1 disponible, 1 en panne, 1 en maintenance)
        res = self.client.get(url_dashboard)
        self.assertEqual(res.context["total_equipements"], 3)
        self.assertEqual(res.context["nb_disponibles"], 1)
        self.assertEqual(res.context["nb_en_panne"], 1)
        self.assertEqual(res.context["nb_en_maintenance"], 1)

        # Ajout d'un équipement disponible
        self.client.post(
            reverse("inventory:equipement_create"),
            data={
                "code_inventaire": "INV-004",
                "designation": "HP ProDesk",
                "categorie": Equipement.Categorie.ORDINATEUR,
                "marque": "HP",
                "date_acquisition": "2024-02-01",
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Salle 101",
            },
        )
        res = self.client.get(url_dashboard)
        self.assertEqual(res.context["total_equipements"], 4)
        self.assertEqual(res.context["nb_disponibles"], 2)

        # Passage de l'équipement en panne -> disponible
        self.client.post(
            reverse("inventory:equipement_update", args=[self.eq_panne.pk]),
            data={
                "code_inventaire": self.eq_panne.code_inventaire,
                "designation": self.eq_panne.designation,
                "categorie": self.eq_panne.categorie,
                "marque": self.eq_panne.marque,
                "date_acquisition": "2023-06-10",
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": self.eq_panne.salle,
            },
        )
        res = self.client.get(url_dashboard)
        self.assertEqual(res.context["nb_disponibles"], 3)
        self.assertEqual(res.context["nb_en_panne"], 0)

        # Suppression d'un équipement en maintenance
        self.client.post(
            reverse("inventory:equipement_delete", args=[self.eq_maint.pk])
        )
        res = self.client.get(url_dashboard)
        self.assertEqual(res.context["total_equipements"], 3)
        self.assertEqual(res.context["nb_en_maintenance"], 0)

    def test_recherche_par_code_et_designation(self):
        """La recherche GET filtre par code d'inventaire ou par désignation."""
        url_liste = reverse("inventory:equipement_list")

        res_code = self.client.get(url_liste, {"q": "inv-002"})
        self.assertContains(res_code, "INV-002")
        self.assertNotContains(res_code, "Dell Latitude 5540")
        self.assertEqual(list(res_code.context["equipements"]), [self.eq_panne])

        res_des = self.client.get(url_liste, {"q": "Latitude"})
        self.assertContains(res_des, "Dell Latitude 5540")
        self.assertNotContains(res_des, "Canon i-SENSYS MF453dw")
        self.assertEqual(list(res_des.context["equipements"]), [self.eq_dispo])

    def test_filtrage_categorie_etat_et_aucun_resultat(self):
        """Les filtres catégorie/état sont combinables et affichent une alerte si vide."""
        url_liste = reverse("inventory:equipement_list")

        res = self.client.get(
            url_liste,
            {
                "categorie": Equipement.Categorie.IMPRIMANTE,
                "etat": Equipement.Etat.EN_PANNE,
            },
        )
        self.assertContains(res, "INV-002")
        self.assertNotContains(res, "Dell Latitude 5540")
        self.assertNotContains(res, "Epson EB-X51")
        self.assertEqual(list(res.context["equipements"]), [self.eq_panne])

        res_vide = self.client.get(url_liste, {"q": "INTROUVABLE-999"})
        self.assertEqual(res_vide.status_code, 200)
        self.assertContains(
            res_vide,
            "Aucun équipement ne correspond aux critères de recherche sélectionnés.",
        )

    def test_suppression_apres_confirmation(self):
        """GET affiche la confirmation sans supprimer ; POST supprime l'équipement."""
        url_suppr = reverse("inventory:equipement_delete", args=[self.eq_dispo.pk])

        res_get = self.client.get(url_suppr)
        self.assertEqual(res_get.status_code, 200)
        self.assertContains(res_get, "Confirmer la suppression")
        self.assertTrue(Equipement.objects.filter(pk=self.eq_dispo.pk).exists())

        res_post = self.client.post(url_suppr, follow=True)
        self.assertEqual(res_post.status_code, 200)
        self.assertFalse(Equipement.objects.filter(pk=self.eq_dispo.pk).exists())

    def test_unicite_code_inventaire(self):
        """Deux équipements ne peuvent pas partager le même code_inventaire."""
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Equipement.objects.create(
                    code_inventaire="INV-001",
                    designation="Doublon",
                    categorie=Equipement.Categorie.AUTRE,
                    marque="Autre",
                    date_acquisition=date(2024, 1, 1),
                    etat=Equipement.Etat.DISPONIBLE,
                    salle="Salle 101",
                )

        # Validation côté formulaire
        response = self.client.post(
            reverse("inventory:equipement_create"),
            data={
                "code_inventaire": "INV-001",
                "designation": "Doublon Formulaire",
                "categorie": Equipement.Categorie.AUTRE,
                "marque": "Autre",
                "date_acquisition": "2024-01-01",
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Salle 101",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Equipement.objects.filter(code_inventaire="INV-001").count(), 1)
