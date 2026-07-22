import csv
import unicodedata
from decimal import Decimal, InvalidOperation

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from .models import Pyme


def _normalize(text):
    text = text or ""
    nfkd = unicodedata.normalize("NFKD", str(text))
    return nfkd.encode("ascii", "ignore").decode("ascii").lower().strip()


def match_choice(value, choices, field_name):
    if not (value or "").strip():
        return ""
    normalized_input = _normalize(value)
    for db_value, label in choices:
        if normalized_input in {_normalize(db_value), _normalize(label)}:
            return db_value
    raise ValidationError(f"{field_name}: valor desconocido '{value}'.")


def parse_coordinate(value, minimum, maximum, label):
    if not (value or "").strip():
        return ""
    normalized = str(value).strip().replace(",", ".")
    try:
        number = float(normalized)
    except ValueError as exc:
        raise ValidationError(f"{label}: coordenada inválida '{value}'.") from exc
    if not minimum <= number <= maximum:
        raise ValidationError(f"{label}: debe estar entre {minimum} y {maximum}.")
    return str(number)


def parse_maturity(row):
    raw_score = (row.get("Puntaje madurez") or row.get("Puntaje de madurez") or "").strip()
    if raw_score:
        try:
            score = Decimal(raw_score.replace(",", "."))
        except InvalidOperation as exc:
            raise ValidationError(f"Puntaje de madurez inválido: '{raw_score}'.") from exc
        if not 0 <= score <= 100:
            raise ValidationError("El puntaje de madurez debe estar entre 0 y 100.")
        return score
    return {"inicial": Decimal("10"), "medio": Decimal("50"), "alto": Decimal("90")}.get(
        _normalize(row.get("Nivel"))
    )


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField(label="Archivo CSV")


@admin.register(Pyme)
class PymeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "province",
        "work_type",
        "enterprise_type",
        "sector",
        "maturity_score",
    )
    list_filter = ("province", "work_type", "enterprise_type", "sector")
    search_fields = ("name", "legal_name", "tax_id", "locality")
    change_list_template = "admin/pyme_changelist.html"

    def get_urls(self):
        return [
            path(
                "import-csv/",
                self.admin_site.admin_view(self.import_csv),
                name="pyme-import-csv",
            )
        ] + super().get_urls()

    def import_csv(self, request):
        form = CsvImportForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            try:
                decoded = form.cleaned_data["csv_upload"].read().decode("utf-8-sig").splitlines()
                reader = csv.DictReader(decoded)
                count = 0
                with transaction.atomic():
                    for row_number, row in enumerate(reader, start=2):
                        name = (row.get("Nombre de Fantasia") or "").strip()
                        if not name:
                            continue
                        tax_id = "".join(filter(str.isdigit, row.get("CUIT") or "")) or None
                        values = {
                            "name": name,
                            "legal_name": (row.get("Nombre Real") or "").strip(),
                            "address": (row.get("Dirección postal") or "").strip(),
                            "locality": (row.get("Localidad") or "").strip(),
                            "province": (row.get("Provincia") or "").strip(),
                            "tax_id": tax_id,
                            "website": (row.get("WEB") or "").strip(),
                            "description": (row.get("Descripción") or "").strip(),
                            "work_type": match_choice(
                                row.get("Trabajo realizado"), Pyme.WorkTypeOptions.choices, "Trabajo realizado"
                            ),
                            "enterprise_type": match_choice(
                                row.get("Tipo de empresa"), Pyme.EnterpriseTypeOptions.choices, "Tipo de empresa"
                            ),
                            "sector": match_choice(row.get("Sector"), Pyme.SectorOptions.choices, "Sector"),
                            "maturity_score": parse_maturity(row),
                            "latitud": parse_coordinate(row.get("Latitud"), -90, 90, "Latitud"),
                            "longitud": parse_coordinate(row.get("Longitud"), -180, 180, "Longitud"),
                        }
                        lookup = {"tax_id": tax_id} if tax_id else {"name": name}
                        pyme, _ = Pyme.objects.update_or_create(**lookup, defaults=values)
                        try:
                            pyme.full_clean()
                        except ValidationError as exc:
                            raise ValidationError(f"Fila {row_number}: {exc}") from exc
                        count += 1
            except (UnicodeDecodeError, ValidationError) as exc:
                form.add_error("csv_upload", str(exc))
            else:
                self.message_user(request, f"Se importaron o actualizaron {count} PyMEs.", messages.SUCCESS)
                return HttpResponseRedirect("../")

        context = self.admin_site.each_context(request)
        context["form"] = form
        return render(request, "admin/csv_form.html", context)
