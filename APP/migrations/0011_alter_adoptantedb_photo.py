# Generated by Django 5.0.6 on 2024-06-21 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0010_alter_adoptantedb_ape_alter_adoptantedb_correo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoptantedb',
            name='photo',
            field=models.ImageField(default='Adoptante_default.png', upload_to='Adoptante/'),
        ),
    ]