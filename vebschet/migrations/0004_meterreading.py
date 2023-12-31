# Generated by Django 4.2 on 2023-06-19 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vebschet', '0003_rename_counter_number_userprofile_counter_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeterReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reading', models.IntegerField()),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vebschet.userprofile')),
            ],
        ),
    ]
