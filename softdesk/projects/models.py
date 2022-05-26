from django.db import models
from django.conf import settings


class Project(models.Model):
    class Type(models.TextChoices):
        BACK_END = 'back-end'
        FRONT_END = 'front-end'
        IOS = 'iOS'
        ANDROID = 'Android'


    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    type = models.CharField(choices=Type.choices, max_length=16)
    author_user_id = models.ForeignKey(
                                       to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='project-author'
                                       )


class Contributor(models.Model):
    class Permission(models.TextChoices):
        AUTHOR = 'Auteur'
        CONTRIBUTOR = 'Contributeur'


    user_id = models.ForeignKey(
                                to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE
                                )
    project_id = models.ForeignKey(
                                   to=Project,
                                   on_delete=models.CASCADE
                                   )
    permission = models.CharField(choices=Permission.choices, max_length=16)
    role = models.CharField(max_length=64)


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
                                       related_name='issue-author'
                                       )
    assignee_user_id = models.ForeignKey(
                                         to=settings.AUTH_USER_MODEL,
                                         on_delete=models.CASCADE,
                                         related_name='issue-assignee'
                                         )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=256)
    author_user_id = models.ForeignKey(
                                       to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='comment-author'
                                       )
    issue_id = models.ForeignKey(
                                 to=Issue,
                                 on_delete=models.CASCADE
                                 )
    created_time = models.DateTimeField(auto_now_add=True)
