# Generated by Django 3.0.5 on 2023-05-06 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.CharField(max_length=30),
        ),
    ]
