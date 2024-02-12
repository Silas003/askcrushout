# Generated by Django 4.2.2 on 2024-02-07 16:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_person_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='response',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.CharField(default='76791', max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]
