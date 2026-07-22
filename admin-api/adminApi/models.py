from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Pyme(models.Model):
    class WorkTypeOptions(models.TextChoices):
        TRANSFORMACION_DIGITAL = "Transformación Digital", "Transformación Digital"
        INNOVACION = "innovación", "Innovación"
        SUSTENTABILIDAD = "Sustentabilidad", "Sustentabilidad"

    class SectorOptions(models.TextChoices):
        SERVICIOS = "Servicios", "Servicios"
        METALURGICO = "Metalúrgico", "Metalúrgico"
        GRAFICO = "Gráfico", "Gráfico"
        FABRICA = "Fabrica", "Fábrica e industrias"
        TEXTIL = "Textil", "Textiles y afines"
        ALIMENTOS = "Alimentos", "Alimentos y afines"

    class EnterpriseTypeOptions(models.TextChoices):
        MICRO_PYME = "Micro-Pyme", "Micro-Pyme"
        PYME = "PyME", "PyME"
        MEDIANA_TRAMO_1 = "Mediana Tramo 1", "Mediana Tramo 1"

    name = models.TextField()
    legal_name = models.TextField(blank=True)
    address = models.TextField(blank=True)
    locality = models.CharField(max_length=120, blank=True)
    province = models.CharField(max_length=120, blank=True)
    tax_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    work_type = models.CharField(
        max_length=100,
        choices=WorkTypeOptions.choices,
        default=WorkTypeOptions.TRANSFORMACION_DIGITAL,
    )
    enterprise_type = models.CharField(
        max_length=50, choices=EnterpriseTypeOptions.choices, blank=True
    )
    sector = models.CharField(max_length=50, choices=SectorOptions.choices, blank=True)
    maturity_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    latitud = models.TextField(blank=True)
    longitud = models.TextField(blank=True)

    class Meta:
        ordering = ("name", "id")
        constraints = [
            models.CheckConstraint(
                condition=Q(maturity_score__isnull=True)
                | Q(maturity_score__gte=0, maturity_score__lte=100),
                name="pyme_maturity_score_between_0_and_100",
            )
        ]

    @property
    def maturity_level(self):
        if self.maturity_score is None:
            return None
        score = Decimal(self.maturity_score)
        return min(5, max(1, int((score - Decimal("0.01")) // 20) + 1))

    @property
    def maturity_band(self):
        level = self.maturity_level
        if level is None:
            return None
        if level <= 2:
            return "Inicial"
        if level <= 4:
            return "Medio"
        return "Alto"

    @property
    def rating(self):
        if self.maturity_score is None:
            return None
        return round(float(self.maturity_score) / 20, 1)

    def __str__(self):
        return f"{self.id} - {self.name}"
