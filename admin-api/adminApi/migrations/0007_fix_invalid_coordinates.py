from django.db import migrations


COORDINATE_CORRECTIONS = {
    "Empresa 1415": ("-34.864912", "-58.618771"),
    "Grupo TCLast SAS": ("-34.622379", "-58.384959"),
    "La Pilarica SA": ("-34.634260", "-58.418607"),
    "Unimer Argentina SA": ("-34.864912", "-58.618771"),
    "Zaplast SA": ("-34.132600", "-59.067875"),
}


def fix_invalid_coordinates(apps, schema_editor):
    pyme_model = apps.get_model("adminApi", "Pyme")
    for name, (latitude, longitude) in COORDINATE_CORRECTIONS.items():
        pyme_model.objects.filter(name=name).update(
            latitud=latitude,
            longitud=longitude,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("adminApi", "0006_pyme_profile_and_maturity_score"),
    ]

    operations = [
        migrations.RunPython(fix_invalid_coordinates, migrations.RunPython.noop),
    ]
