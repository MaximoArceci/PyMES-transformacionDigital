from decimal import Decimal

from django.db import migrations, models
import django.core.validators
from django.db.models import Q


def migrate_legacy_data(apps, schema_editor):
    Pyme = apps.get_model("adminApi", "Pyme")
    score_by_band = {"inicial": Decimal("10"), "medio": Decimal("50"), "alto": Decimal("90")}
    for pyme in Pyme.objects.all().iterator():
        pyme.name = pyme.name or f"Empresa {pyme.pk}"
        pyme.enterprise_type = pyme.enterprise_type or ""
        pyme.sector = pyme.sector or ""
        pyme.latitud = pyme.latitud or ""
        pyme.longitud = pyme.longitud or ""
        pyme.maturity_score = score_by_band.get((pyme.nivelMaduracion or "").lower())
        pyme.save(
            update_fields=(
                "name",
                "enterprise_type",
                "sector",
                "latitud",
                "longitud",
                "maturity_score",
            )
        )


class Migration(migrations.Migration):
    dependencies = [("adminApi", "0005_alter_pyme_work_type")]

    operations = [
        migrations.AddField(model_name="pyme", name="address", field=models.TextField(blank=True)),
        migrations.AddField(model_name="pyme", name="description", field=models.TextField(blank=True)),
        migrations.AddField(model_name="pyme", name="legal_name", field=models.TextField(blank=True)),
        migrations.AddField(model_name="pyme", name="locality", field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(
            model_name="pyme",
            name="maturity_score",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=5,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
        ),
        migrations.AddField(model_name="pyme", name="province", field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(
            model_name="pyme",
            name="tax_id",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AddField(model_name="pyme", name="website", field=models.URLField(blank=True)),
        migrations.RunPython(migrate_legacy_data, migrations.RunPython.noop),
        migrations.AlterField(model_name="pyme", name="name", field=models.TextField()),
        migrations.AlterField(model_name="pyme", name="latitud", field=models.TextField(blank=True)),
        migrations.AlterField(model_name="pyme", name="longitud", field=models.TextField(blank=True)),
        migrations.AlterField(
            model_name="pyme",
            name="enterprise_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Micro-Pyme", "Micro-Pyme"),
                    ("PyME", "PyME"),
                    ("Mediana Tramo 1", "Mediana Tramo 1"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="pyme",
            name="sector",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Servicios", "Servicios"),
                    ("Metalúrgico", "Metalúrgico"),
                    ("Gráfico", "Gráfico"),
                    ("Fabrica", "Fábrica e industrias"),
                    ("Textil", "Textiles y afines"),
                    ("Alimentos", "Alimentos y afines"),
                ],
                max_length=50,
            ),
        ),
        migrations.RemoveField(model_name="pyme", name="nivelMaduracion"),
        migrations.AddConstraint(
            model_name="pyme",
            constraint=models.CheckConstraint(
                condition=Q(maturity_score__isnull=True)
                | Q(maturity_score__gte=0, maturity_score__lte=100),
                name="pyme_maturity_score_between_0_and_100",
            ),
        ),
        migrations.AlterModelOptions(name="pyme", options={"ordering": ("name", "id")}),
    ]
