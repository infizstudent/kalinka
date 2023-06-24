# Generated by Django 4.2 on 2023-06-24 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vebschet', '0009_delete_electricitycost'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricityPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]