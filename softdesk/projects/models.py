from django.db import models, transaction
from django.db.models import F
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
                                related_name='project_contributors'
                                )
    project_id = models.ForeignKey(
                                   to=Project,
                                   on_delete=models.CASCADE,
                                   related_name='contributor_list'
                                   )
    permission = models.CharField(choices=Permission.choices, max_length=16)
    role = models.CharField(max_length=64)

    class Meta:
        unique_together = ('user_id', 'project_id',)

    def __str__(self):
        return f"{self.user_id}:{self.permission} ({self.role})"

    @transaction.atomic
    def delete(self):
        """
        When a contributor is removed from a project, all it's contributions
        are deleted and it's assignements are set back to the issue's author.
        """
        user_issues = Issue.objects.filter(project_id=self.project_id,
                                           author_user_id=self.user_id)
        user_comments = Comment.objects.filter(project_id=self.project_id,
                                               author_user_id=self.user_id)
        assignements = Issue.objects.filter(project_id=self.project_id,
                                            assignee_user_id=self.user_id)
        assignements.update(assignee_user_id=F('author_user_id'))
        user_issues.delete()
        user_comments.delete()
        return super().delete()


class Issue(models.Model):
    class Tag(models.TextChoices):
        BUG = 'BUG'
        REFACTOR = 'AMELIORER'
        TODO = 'TACHE'

    class Priority(models.TextChoices):
        LOW = 'FAIBLE'
        MEDIUM = 'MOYENNE'
        HIGH = 'ELEVEE'

    class Status(models.TextChoices):
        TO_BE_DONE = 'A faire'
        IN_PROGRESS = 'En cours'
        DONE = 'Termin??'

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    tag = models.CharField(choices=Tag.choices, max_length=16)
    priority = models.CharField(choices=Priority.choices, max_length=16)
    project_id = models.ForeignKey(
                                   to=Project,
                                   on_delete=models.CASCADE,
                                   related_name='project_issue'
                                   )
    status = models.CharField(choices=Status.choices, max_length=16)
    author_user_id = models.ForeignKey(
                                       to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='issue_author'
                                       )
    assignee_user_id = models.ForeignKey(
                                         to=settings.AUTH_USER_MODEL,
                                         null=True,
                                         on_delete=models.SET_NULL,
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
    project_id = models.ForeignKey(
                                   default=0,
                                   to=Project,
                                   on_delete=models.CASCADE,
                                   )
    issue_id = models.ForeignKey(
                                 to=Issue,
                                 on_delete=models.CASCADE,
                                 related_name='issue_comment'
                                 )
    created_time = models.DateTimeField(auto_now_add=True)
