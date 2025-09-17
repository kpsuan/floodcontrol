from django.db import migrations
from datetime import date

def seed_projects(apps, schema_editor):
    FloodControl = apps.get_model("floodapp", "FloodControl")
    if FloodControl.objects.count() == 0:
        FloodControl.objects.bulk_create([
            FloodControl(
                description="Construction of Flood Mitigation Structure along Agusan River (Dankias Section) Package 1, Butuan City",
                location="AGUSAN DEL NORTE",
                contractor="ME 3 CONSTRUCTION",
                cost=137272357.59,
                completion_date=date(2025, 5, 30),
            ),
            FloodControl(
                description="Construction of Bank Protection, Lower Agusan River, Barangay Golden Ribbon, Butuan City",
                location="AGUSAN DEL NORTE",
                contractor="RAMISES CONSTRUCTION",
                cost=96158174.50,
                completion_date=date(2025, 5, 30),
            ),
        ])

def undo_seed(apps, schema_editor):
    FloodControl = apps.get_model("floodapp", "FloodControl")
    FloodControl.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ("floodapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_projects, undo_seed),
    ]
