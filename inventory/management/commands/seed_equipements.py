"""
Commande de management Django pour peupler la base de données avec un jeu
d'équipements réalistes de démonstration.
Utilisation : python manage.py seed_equipements
"""

from datetime import date

from django.core.management.base import BaseCommand

from inventory.models import Equipement


class Command(BaseCommand):
    """Insère ou met à jour les équipements initiaux de l'ISEP."""

    help = "Charge au moins 10 équipements réalistes dans la base de données."

    def handle(self, *args, **options):
        equipements_initiaux = [
            {
                "code_inventaire": "INV-001",
                "designation": "Dell Latitude 5540",
                "categorie": Equipement.Categorie.ORDINATEUR,
                "marque": "Dell",
                "numero_serie": "DL5540-SN-001",
                "date_acquisition": date(2024, 3, 15),
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Labo Info",
                "observations": "Intel Core i7, 16 Go RAM, SSD 512 Go, écran 15,6 pouces.",
            },
            {
                "code_inventaire": "INV-002",
                "designation": "HP ProDesk 400 G9",
                "categorie": Equipement.Categorie.ORDINATEUR,
                "marque": "HP",
                "numero_serie": "HP400G9-SN-002",
                "date_acquisition": date(2023, 11, 8),
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Salle 101",
                "observations": "Poste fixe avec écran 24 pouces, clavier et souris filaires.",
            },
            {
                "code_inventaire": "INV-003",
                "designation": "Lenovo ThinkPad T14",
                "categorie": Equipement.Categorie.ORDINATEUR,
                "marque": "Lenovo",
                "numero_serie": "LNT14-SN-003",
                "date_acquisition": date(2024, 1, 22),
                "etat": Equipement.Etat.EN_MAINTENANCE,
                "salle": "Bureau Direction",
                "observations": "Remplacement batterie et mise à jour BIOS en cours.",
            },
            {
                "code_inventaire": "INV-004",
                "designation": "HP LaserJet Pro M404dn",
                "categorie": Equipement.Categorie.IMPRIMANTE,
                "marque": "HP",
                "numero_serie": "HPM404-SN-004",
                "date_acquisition": date(2023, 6, 12),
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Secrétariat",
                "observations": "Imprimante laser monochrome recto-verso réseau.",
            },
            {
                "code_inventaire": "INV-005",
                "designation": "Canon i-SENSYS MF453dw",
                "categorie": Equipement.Categorie.IMPRIMANTE,
                "marque": "Canon",
                "numero_serie": "CNMF453-SN-005",
                "date_acquisition": date(2022, 9, 30),
                "etat": Equipement.Etat.EN_PANNE,
                "salle": "Bureau Direction",
                "observations": "Bourrage papier récurrent au niveau du bac 1.",
            },
            {
                "code_inventaire": "INV-006",
                "designation": "Epson EB-X51",
                "categorie": Equipement.Categorie.VIDEOPROJECTEUR,
                "marque": "Epson",
                "numero_serie": "EPX51-SN-006",
                "date_acquisition": date(2023, 10, 5),
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Salle 101",
                "observations": "3800 lumens, HDMI/VGA, fourni avec télécommande et sacoche.",
            },
            {
                "code_inventaire": "INV-007",
                "designation": "BenQ MH560",
                "categorie": Equipement.Categorie.VIDEOPROJECTEUR,
                "marque": "BenQ",
                "numero_serie": "BQ560-SN-007",
                "date_acquisition": date(2022, 4, 19),
                "etat": Equipement.Etat.EN_MAINTENANCE,
                "salle": "Amphi A",
                "observations": "Nettoyage optique et remplacement de la lampe prévus.",
            },
            {
                "code_inventaire": "INV-008",
                "designation": "Switch Cisco Catalyst 2960-X",
                "categorie": Equipement.Categorie.RESEAU,
                "marque": "Cisco",
                "numero_serie": "CS2960X-SN-008",
                "date_acquisition": date(2024, 2, 10),
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Baie Réseau",
                "observations": "24 ports Gigabit PoE+ avec 4 ports SFP uplink.",
            },
            {
                "code_inventaire": "INV-009",
                "designation": "Routeur MikroTik RB4011",
                "categorie": Equipement.Categorie.RESEAU,
                "marque": "MikroTik",
                "numero_serie": "MTRB4011-SN-009",
                "date_acquisition": date(2023, 8, 17),
                "etat": Equipement.Etat.EN_PANNE,
                "salle": "Labo Info",
                "observations": "Alimentation DC défectueuse suite à une surtension.",
            },
            {
                "code_inventaire": "INV-010",
                "designation": "Onduleur APC Smart-UPS 1500VA",
                "categorie": Equipement.Categorie.AUTRE,
                "marque": "APC",
                "numero_serie": "APC1500-SN-010",
                "date_acquisition": date(2024, 5, 3),
                "etat": Equipement.Etat.DISPONIBLE,
                "salle": "Baie Réseau",
                "observations": "Protection électrique des équipements cœur de réseau.",
            },
        ]

        crees = 0
        mis_a_jour = 0

        for data in equipements_initiaux:
            _, created = Equipement.objects.update_or_create(
                code_inventaire=data["code_inventaire"],
                defaults=data,
            )
            if created:
                crees += 1
            else:
                mis_a_jour += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Initialisation terminée : {crees} équipement(s) créé(s), "
                f"{mis_a_jour} mis à jour."
            )
        )
