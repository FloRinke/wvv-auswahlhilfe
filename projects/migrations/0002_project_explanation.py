# Generated by Django 3.0.4 on 2020-03-20 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='explanation',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
