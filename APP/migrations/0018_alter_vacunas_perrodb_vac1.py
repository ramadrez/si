# Generated by Django 5.0.6 on 2024-06-21 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0017_vacunas_perrodb_vac2_vacunas_perrodb_vac3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacunas_perrodb',
            name='vac1',
            field=models.CharField(default=None, max_length=50, verbose_name='Parvovirus'),
        ),
    ]