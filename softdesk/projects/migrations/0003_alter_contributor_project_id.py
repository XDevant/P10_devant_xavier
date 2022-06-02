# Generated by Django 4.0.4 on 2022-05-31 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_contributor_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_list', to='projects.project'),
        ),
    ]