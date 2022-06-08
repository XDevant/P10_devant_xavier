from rest_framework.viewsets import ModelViewSet
from projects.models import Project, Issue, Comment, Contributor
from projects.serializers import ProjectSerializerSelector,\
                                 IssueSerializerSelector,\
                                 ContributorSerializerSelector,\
                                 CommentSerializerSelector
from projects.permissions import IsContributor, IsAuthorOrReadOnly, IsProjectAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


class MultipleSerializerMixin:
    serializer_class = None
    multi_serializer_class = None
    detail = False

    def get_serializer_class(self):
        if self.multi_serializer_class is not None and self.detail:
            return self.multi_serializer_class.detail
        return self.serializer_class


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializerSelector.list
    multi_serializer_class = ProjectSerializerSelector
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Project.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(author_user_id=request.user)
        project.contributors.add(
                                request.user,
                                through_defaults={
                                                  'permission': 'Auteur',
                                                  'role': "Chef de projet"
                                                  }
                                )
        headers = self.get_success_headers(serializer.data)
        return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers
                        )

    def partial_update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        queryset = super(ProjectViewSet, self).get_queryset()
        user =  self.request.user
        user_id = getattr(user, 'user_id')
        if isinstance(user, User):
            return queryset.filter(contributors__user_id=user_id)

    def get_serializer_class(self):
        if self.multi_serializer_class is not None and self.detail:
            return self.multi_serializer_class.detail
        return self.serializer_class


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorSerializerSelector.list
    multi_serializer_class = ContributorSerializerSelector
    permission_classes = [IsAuthenticated, IsProjectAuthorOrReadOnly, IsContributor]

    def perform_create(self, serializer):
        project = Project.objects.get(project_id=self.kwargs["projects_pk"])
        try:
            new_email = serializer.initial_data['user_id']
            new_contributor = User.objects.get(email=new_email)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if Contributor.objects.filter(
                                      user_id=new_contributor,
                                      project_id=project
                                      ).exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.save(
                        user_id=new_contributor,
                        project_id=project,
                        permission="Contributeur"
                        )

    def update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.get(project_id=self.kwargs["projects_pk"])
        if 'assignee_user_id' in  serializer.initial_data.keys():
            try:
                user_id = serializer.initial_data['assignee_user_id']
                assignee = User.objects.get(user_id=user_id)
            except Exception:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            assignee = request.user
        serializer.save(
                        assignee_user_id=assignee,
                        author_user_id=request.user,
                        project_id=project
                        )
        headers = self.get_success_headers(serializer.data)
        return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers
                        )

    def partial_update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
    def get_queryset(self):
        project_pk = self.kwargs["projects_pk"]
        return Issue.objects.filter(project_id=project_pk)


class CommentViewSet(ModelViewSet):
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
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        issue_pk = self.kwargs["issues_pk"]
        project_pk = self.kwargs["projects_pk"]
        return Comment.objects.filter(issue_id=issue_pk, project_id = project_pk)
