from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from projects.models import Project, Issue, Comment
from projects.serializers import ProjectSerializerSelector, IssueSerializerSelector,\
                                 ContributorListSerializer, CommentListSerializer
from softdesk.projects.permissions import IsContributor, IsProjectAuthorOrCR


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
    permission_classes = [IsContributor, IsProjectAuthorOrCR]
 
    def get_queryset(self):
        return Project.objects.all()


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorListSerializer


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueSerializerSelector.list
    multi_serializer_class = IssueSerializerSelector
 
    def get_queryset(self):
        return Issue.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentListSerializer
 
    def get_queryset(self):
        return Comment.objects.all()
