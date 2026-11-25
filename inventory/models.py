"""
Modèles de données de l'application inventory.
Définit le modèle Equipement pour le suivi du matériel informatique de l'ISEP.
"""

from django.db import models


class Equipement(models.Model):
    """Représente un équipement informatique ou audiovisuel inventorié."""

    class Categorie(models.TextChoices):
        ORDINATEUR = "Ordinateur", "Ordinateur"
        IMPRIMANTE = "Imprimante", "Imprimante"
        VIDEOPROJECTEUR = "Vidéoprojecteur", "Vidéoprojecteur"
        RESEAU = "Réseau", "Réseau"
        AUTRE = "Autre", "Autre"

    class Etat(models.TextChoices):
        DISPONIBLE = "Disponible", "Disponible"
        EN_PANNE = "En panne", "En panne"
        EN_MAINTENANCE = "En maintenance", "En maintenance"

    code_inventaire = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Code d'inventaire",
        help_text="Identifiant unique de l'équipement (ex. INV-001).",
    )
    designation = models.CharField(
        max_length=150,
        verbose_name="Désignation",
    )
    categorie = models.CharField(
        max_length=30,
        choices=Categorie.choices,
        default=Categorie.ORDINATEUR,
        verbose_name="Catégorie",
    )
    marque = models.CharField(
        max_length=80,
        verbose_name="Marque",
    )
    numero_serie = models.CharField(
        max_length=80,
        blank=True,
        default="",
        verbose_name="Numéro de série",
    )
    date_acquisition = models.DateField(
        verbose_name="Date d'acquisition",
    )
    etat = models.CharField(
        max_length=30,
        choices=Etat.choices,
        default=Etat.DISPONIBLE,
        verbose_name="État",
    )
    salle = models.CharField(
        max_length=100,
        verbose_name="Salle / Emplacement",
    )
    image = models.ImageField(
        upload_to="equipements/",
        blank=True,
        null=True,
        verbose_name="Image de l'équipement",
        help_text="Photo de l'équipement (facultatif : une illustration par défaut est affichée sinon).",
    )
    observations = models.TextField(
        blank=True,
        default="",
        verbose_name="Détails techniques / Observations",
    )

    class Meta:
        ordering = ["code_inventaire"]
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"

    def __str__(self):
        return f"{self.code_inventaire} - {self.designation}"

    @property
    def default_image_path(self):
        """Retourne le chemin statique de l'illustration correspondant à la catégorie."""
        mapping = {
            self.Categorie.ORDINATEUR: "inventory/img/ordinateur.svg",
            self.Categorie.IMPRIMANTE: "inventory/img/imprimante.svg",
            self.Categorie.VIDEOPROJECTEUR: "inventory/img/videoprojecteur.svg",
            self.Categorie.RESEAU: "inventory/img/reseau.svg",
            self.Categorie.AUTRE: "inventory/img/autre.svg",
        }
        return mapping.get(self.categorie, "inventory/img/autre.svg")
