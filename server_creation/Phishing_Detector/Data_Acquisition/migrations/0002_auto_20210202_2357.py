# Generated by Django 3.1.5 on 2021-02-02 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Data_Acquisition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phishtank_urls',
            name='URL_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Data_Acquisition.urls', unique=True),
        ),
    ]
