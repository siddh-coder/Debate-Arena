# Generated by Django 5.1.7 on 2025-03-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='debate',
            name='code',
            field=models.CharField(blank=True, max_length=6, unique=True),
        ),
    ]
