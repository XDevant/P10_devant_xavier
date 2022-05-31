from rest_framework.viewsets import ModelViewSet
from projects.models import Project, Issue, Comment, Contributor
from projects.serializers import ProjectSerializerSelector, IssueSerializerSelector,\
                                 ContributorListSerializer, CommentListSerializer
from projects.permissions import IsContributor, IsAuthorOrReadOnly
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


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectSerializerSelector.list
    multi_serializer_class = ProjectSerializerSelector

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(request))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object(request)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def partial_update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(request)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self, request):
        user_id = request.user.user_id
        return Project.objects.filter(contributor__user_id=user_id)

    def get_object(self, request):
        """
        Returns the object the view is displaying.
        Override of the generic method with request arg for get_queryset
        """
        queryset = self.filter_queryset(self.get_queryset(request))
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
            )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorListSerializer

    def partial_update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self, request):
        user_id = request.user.user_id
        return Contributor.objects.filter(user_id=user_id)

class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueSerializerSelector.list
    multi_serializer_class = IssueSerializerSelector

    def partial_update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
 
    def get_queryset(self, request):
        projects_pk = self.kwargs["projects_pk"]
        user_id = request.user.user_id
        return Issue.objects.filter(project_id=projects_pk)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentListSerializer

    def partial_update(self, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        return Comment.objects.all()
