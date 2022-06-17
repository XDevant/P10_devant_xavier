from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from authentication.models import User
from projects.models import Project, Issue, Comment, Contributor
from projects.serializers import ProjectSerializerSelector,\
                                 IssueSerializerSelector,\
                                 ContributorSerializerSelector,\
                                 CommentSerializerSelector
from projects.permissions import IsContributor,\
                                 IsAuthorOrReadOnly,\
                                 IsProjectAuthorOrReadOnly


class MultipleSerializerMixin:
    serializer_class = None
    multi_serializer_class = None
    detail = False

    def get_serializer_class(self):
        if self.multi_serializer_class is not None and self.detail:
            return self.multi_serializer_class.detail
        return self.serializer_class


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectSerializerSelector.list
    multi_serializer_class = ProjectSerializerSelector
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        """
        We fill the contributor through table while we save the new project
        """
        current_user = self.request.user
        project = serializer.save(author_user_id=current_user)
        project.contributors.add(
                                current_user,
                                through_defaults={
                                                  'permission': 'Auteur',
                                                  'role': "Chef de projet"
                                                  }
                                )

    def partial_update(self, *args, **kwargs):
        """This method is not implemented"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        """We filter the project list to show only the projects the user is
        contributor of."""
        queryset = super(ProjectViewSet, self).get_queryset()
        user = self.request.user
        user_id = getattr(user, 'user_id')
        if isinstance(user, User):
            return queryset.filter(contributors__user_id=user_id)
        return None


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializerSelector.list
    multi_serializer_class = ContributorSerializerSelector
    permission_classes = [IsAuthenticated,
                          IsProjectAuthorOrReadOnly,
                          IsContributor]

    def perform_create(self, serializer):
        project = Project.objects.get(project_id=self.kwargs["projects_pk"])
        try:
            new_email = serializer.initial_data['email']
            new_contributor = User.objects.get(email=new_email)
        except Exception:
            raise ValidationError("Email not found")
        if Contributor.objects.filter(
                                      user_id=new_contributor,
                                      project_id=project
                                      ).exists():
            raise ValidationError("Target is already contributor")
        serializer.save(
                        user_id=new_contributor,
                        project_id=project,
                        permission="Contributeur"
                        )

    def update(self, *args, **kwargs):
        """This method is not implemented"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """We override the method to forbid the Author to delete it's
        contribution and create an orphean project."""
        instance = self.get_object()
        if instance.permission == "Auteur":
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        project_pk = self.kwargs['projects_pk']
        return Contributor.objects.filter(project_id=project_pk)

    def get_serializer_class(self):
        if self.detail:
            return self.multi_serializer_class.detail
        elif self.action == 'create':
            return self.multi_serializer_class.create
        return self.serializer_class


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueSerializerSelector.list
    multi_serializer_class = IssueSerializerSelector
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, IsContributor]

    def perform_create(self, serializer):
        project = Project.objects.get(project_id=self.kwargs["projects_pk"])
        if 'assignee_email' in serializer.initial_data.keys():
            try:
                assignee_email = serializer.initial_data['assignee_email']
                assignee = User.objects.get(email=assignee_email)
                Contributor.objects.get(user_id=assignee,
                                        project_id=project)
            except Exception:
                message = "assignee_email must be a valid contributor email"
                raise ValidationError(message)
        else:
            assignee = self.request.user
        serializer.save(
                        assignee_user_id=assignee,
                        author_user_id=self.request.user,
                        project_id=project
                        )

    def perform_update(self, serializer):
        self.perform_create(serializer)

    def partial_update(self, *args, **kwargs):
        """This method is not implemented"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        project_pk = self.kwargs["projects_pk"]
        return Issue.objects.filter(project_id=project_pk)


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentSerializerSelector.list
    multi_serializer_class = CommentSerializerSelector
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, IsContributor]

    def perform_create(self, serializer):
        current_user = self.request.user
        project = Project.objects.get(project_id=self.kwargs["projects_pk"])
        issue = Issue.objects.get(id=self.kwargs["issues_pk"])
        serializer.save(
                        author_user_id=current_user,
                        project_id=project,
                        issue_id=issue
                        )

    def partial_update(self, *args, **kwargs):
        """This method is not implemented"""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        issue_pk = self.kwargs["issues_pk"]
        project_pk = self.kwargs["projects_pk"]
        return Comment.objects.filter(issue_id=issue_pk, project_id=project_pk)
