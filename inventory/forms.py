"""
Formulaires de l'application inventory.
Utilise un ModelForm Bootstrap 5 pour la création et la modification d'équipements.
"""

from django import forms

from .models import Equipement


class EquipementForm(forms.ModelForm):
    """Formulaire Bootstrap pour ajouter ou modifier un équipement."""

    class Meta:
        model = Equipement
        fields = [
            "code_inventaire",
            "designation",
            "categorie",
            "marque",
            "numero_serie",
            "date_acquisition",
            "etat",
            "salle",
            "image",
            "observations",
        ]
        widgets = {
            "code_inventaire": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. INV-011",
                }
            ),
            "designation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. Dell Latitude 5540",
                }
            ),
            "categorie": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "marque": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. Dell, HP, Epson, Cisco...",
                }
            ),
            "numero_serie": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. SN-DL5540-9821 (facultatif)",
                }
            ),
            "date_acquisition": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "etat": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "salle": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex. Salle 101, Labo Info...",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "observations": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Caractéristiques techniques, état détaillé, accessoires...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garantit l'acceptation et le pré-remplissage au format ISO du champ date HTML5
        self.fields["date_acquisition"].input_formats = ["%Y-%m-%d"]
