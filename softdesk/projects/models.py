from django.db import models
from django.conf import settings
from authentication.models import User


class Project(models.Model):
    class Type(models.TextChoices):
        BACK_END = 'back-end'
        FRONT_END = 'front-end'
        IOS = 'iOS'
        ANDROID = 'Android'


    project_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    type = models.CharField(choices=Type.choices, max_length=16)
    author_user_id = models.ForeignKey(
                                       to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='project_author'
                                       )
    contributors = models.ManyToManyField(User, through='Contributor')

    def __str__(self):
        return f"{self.title} {self.type} auteur:{self.author_user_id}"


class Contributor(models.Model):
    class Permission(models.TextChoices):
        AUTHOR = 'Auteur'
        CONTRIBUTOR = 'Contributeur'


    user_id = models.ForeignKey(
                                to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                )
    project_id = models.ForeignKey(
                                   to=Project,
                                   on_delete=models.CASCADE,
                                   related_name='contributor_list'
                                   )
    permission = models.CharField(choices=Permission.choices, max_length=16)
    role = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user_id}:{self.permission} ({self.role})"


class Issue(models.Model):
    class Tag(models.TextChoices):
        BUG = 'BUG'
        REFACTOR = 'AMELIORER'
        TODO = 'TÄCHE'


    class Priority(models.TextChoices):
        LOW = 'FAIBLE'
        MEDIUM = 'MOYENNE'
        HIGH = 'ELEVEE'


    class Status(models.TextChoices):
        TO_BE_DONE = 'A faire'
        IN_PROGRESS = 'En cours'
        DONE = 'Terminé'


    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    tag = models.CharField(choices=Tag.choices, max_length=16)
    priority = models.CharField(choices=Priority.choices, max_length=16)
    project_id = models.ForeignKey(
                                   to=Project,
                                   on_delete=models.CASCADE
                                   )
    status = models.CharField(choices=Status.choices, max_length=16)
    author_user_id = models.ForeignKey(
                                       to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='issue_author'
                                       )
    assignee_user_id = models.ForeignKey(
                                         to=settings.AUTH_USER_MODEL,
                                         on_delete=models.CASCADE,
                                         related_name='issue_assignee'
                                         )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=256)
    author_user_id = models.ForeignKey(
                                       to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='comment_author'
                                       )
    issue_id = models.ForeignKey(
                                 to=Issue,
                                 on_delete=models.CASCADE
                                 )
    created_time = models.DateTimeField(auto_now_add=True)
