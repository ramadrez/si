# Generated by Django 5.1.1 on 2024-10-12 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0043_alter_animalesdb_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adopcionesdb',
            name='id',
            field=models.AutoField(default=None, primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='animalesdb',
            name='id',
            field=models.AutoField(default=None, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
