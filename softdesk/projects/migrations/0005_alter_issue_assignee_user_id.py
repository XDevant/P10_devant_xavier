# Generated by Django 4.0.4 on 2022-05-31 23:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0004_alter_contributor_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee_user_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
