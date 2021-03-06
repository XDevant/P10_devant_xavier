# Generated by Django 4.0.4 on 2022-06-02 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0006_alter_issue_assignee_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='project_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_contributors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='tag',
            field=models.CharField(choices=[('BUG', 'Bug'), ('AMELIORER', 'Refactor'), ('TACHE', 'Todo')], max_length=16),
        ),
    ]
