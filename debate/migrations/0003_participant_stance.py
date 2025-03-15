# Generated by Django 5.1.7 on 2025-03-15 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0002_debate_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='stance',
            field=models.CharField(choices=[('for', 'For'), ('against', 'Against')], default='for', max_length=7),
        ),
    ]
