# Generated by Django 4.2.7 on 2023-12-04 04:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default=django.utils.timezone.now, max_length=254, verbose_name='email address'),
            preserve_default=False,
        ),
    ]
