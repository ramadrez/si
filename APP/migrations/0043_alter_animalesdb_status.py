# Generated by Django 5.1.1 on 2024-10-07 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0042_alter_adopcionesdb_animal_animalesdb_fk_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalesdb',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Status_adopcion'),
        ),
    ]
