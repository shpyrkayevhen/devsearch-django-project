# Generated by Django 4.0.6 on 2022-08-01 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created']},
        ),
    ]
