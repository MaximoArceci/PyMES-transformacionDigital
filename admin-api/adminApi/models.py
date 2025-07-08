from django.db import models

class Pyme(models.Model):

    class WorkTypeOptions(models.TextChoices):
        TRANSFORMACION_DIGITAL = 'Transformación Digital', 'Transformación Digital'
        INNOVACION = 'innovacion', 'Innovación'
        SUSTENTABILIDAD = 'Sustentabilidad', 'Sustentabilidad'

    class NivelMaduracionOptions(models.TextChoices):
        INICIAL = 'inicial'
        MEDIO = 'medio'
        ALTO = 'alto'

    class SectorOptions(models.TextChoices):
        SERVICIOS = 'Servicios', 'Servicios'
        METALURGICO = 'Metalúrgico', 'Metalúrgico'
        GRAFICO = 'Gráfico', 'Gráfico'
        FABRICA = 'Fabrica', 'Fábrica'
        TEXTIL = 'Textil', 'Textil'
        ALIMENTOS = 'Alimentos', 'Alimentos'

    class EnterpriseTypeOptions(models.TextChoices):
        MICRO_PYME = 'Micro-Pyme', 'Micro-Pyme'
        PYME = 'PyME', 'PyME'
        MEDIANA_TRAMO_1 = 'Mediana Tramo 1', 'Mediana Tramo 1'

    name = models.TextField(blank=True, null=True)

    work_type = models.CharField(
        max_length=100,
        choices=WorkTypeOptions.choices,
        default=WorkTypeOptions.TRANSFORMACION_DIGITAL,
    )

    enterprise_type = models.CharField(
        max_length=50,
        choices=EnterpriseTypeOptions.choices,
        blank=True,
        null=True,
    )

    sector = models.CharField(
        max_length=50,
        choices=SectorOptions.choices,
        blank=True,
        null=True,
    )

    nivelMaduracion = models.CharField(
        max_length=20,
        choices=NivelMaduracionOptions.choices,
        blank=True,
        null=True,
    )

    latitud = models.TextField(blank=True, null=True)
    longitud = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
