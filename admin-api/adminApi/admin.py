import csv
import unicodedata
from django import forms
from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib import admin
from django.apps import apps
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
# from rest_framework.authtoken.models import TokenProxy  # No se usa, y da error si no está DRF
from .models import Pyme


def _normalize(text: str) -> str:
    """Elimina tildes, convierte a minúsculas y quita espacios extra."""
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_text = nfkd.encode("ascii", "ignore").decode("ascii")
    return ascii_text.lower().strip()


def match_choice(value: str, choices) -> str:
    """
    Intenta encontrar el valor de la BD cuya representación normalizada
    coincida con el texto normalizado que viene del CSV.
    Devuelve el valor original (db_value) si hay match, o el valor
    original recibido si no hay ninguno.
    """
    normalized_input = _normalize(value)
    for db_value, _label in choices:
        if _normalize(db_value) == normalized_input:
            return db_value
    return value

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField(label="Archivo CSV")

@admin.register(Pyme)
class PymeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "work_type", "enterprise_type", "sector", "nivelMaduracion")
    change_list_template = "admin/pyme_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name="pyme-import-csv"),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data["csv_upload"]
                decoded_file = csv_file.read().decode("utf-8").splitlines()
                reader = csv.DictReader(decoded_file)
                count = 0
                for row in reader:
                    if row.get("Nombre de Fantasia") is None or row.get("Nombre de Fantasia") == "":
                        continue
                    Pyme.objects.create(
                        name=row.get("Nombre de Fantasia", ""),
                        work_type=match_choice(
                            row.get("Trabajo realizado", ""),
                            Pyme.WorkTypeOptions.choices,
                        ),
                        enterprise_type=match_choice(
                            row.get("Tipo de empresa", ""),
                            Pyme.EnterpriseTypeOptions.choices,
                        ),
                        sector=match_choice(
                            row.get("Sector", ""),
                            Pyme.SectorOptions.choices,
                        ),
                        nivelMaduracion=match_choice(
                            row.get("Nivel", ""),
                            Pyme.NivelMaduracionOptions.choices,
                        ),
                        latitud=row.get("Latitud", ""),
                        longitud=row.get("Longitud", ""),
                    )
                    count += 1
                self.message_user(request, f"Se importaron {count} pymes correctamente.", messages.SUCCESS)
                return HttpResponseRedirect("../")
        else:
            form = CsvImportForm()
        context = self.admin_site.each_context(request)
        context["form"] = form
        return render(request, "admin/csv_form.html", context)