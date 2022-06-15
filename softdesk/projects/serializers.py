from rest_framework import serializers
from projects.models import Project, Issue, Comment, Contributor
from authentication.models import User


class ChoiceField(serializers.ChoiceField):
    """For all choice fields we make sure not to be case sensitive and provide
    adequate feedback."""
    def to_internal_value(self, data):
        for key in self._choices.keys():
            if key.lower() == data.lower():
                return key
        keys = list(self.choices.keys())
        message = f"{self.field_name} must be one of the following: {keys}"
        raise serializers.ValidationError({'ValueError': message})

class ContributorFilteredPKRF(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        view = self.context.get('view', None)
        queryset = super(ContributorFilteredPKRF, self).get_queryset()
        if not view or not queryset:
            return None
        project_id = view.kwargs['projects_pk']
        qset = queryset.filter(project_contributors__project_id=project_id)
        return qset


class ContributorListSerializer(serializers.ModelSerializer):
    """We only send user (user full name, email) and role.
    Permission field is auto-added, author is identified by his role:
    'Chef de projet'."""
    user = serializers.StringRelatedField(source='user_id')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'role']
        read_only_fields = ['user']


class ContributorCreateSerializer(serializers.ModelSerializer):
    """Project authors can add new contributors via their email only."""
    email = serializers.EmailField(source='user_id', max_length=140)

    class Meta:
        model = Contributor
        fields = ['id', 'email', 'role', 'project_id']
        read_only_fields = ['project_id']


class ContributorDetailSerializer(ContributorListSerializer):
    """Read only, we can not update contributors, only retrieve/delete them"""
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project_id', 'permission', 'role']
        read_only_fields = ['user', 'project_id', 'permission', 'role']


class ContributorSerializerSelector:
    """Import container for the view and it's get_serializer method"""
    list = ContributorListSerializer
    detail = ContributorDetailSerializer
    create = ContributorCreateSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
                                            source='author_user_id',
                                            read_only=True
                                            )
    type = ChoiceField(choices=Project.Type.choices)

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author']
        read_only_fields = ['author']
        

class ProjectDetailSerializer(ProjectListSerializer):
    """Inhérits author and type from the list serializer """
    contributor_list = ContributorListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['project_id',
                  'title',
                  'description',
                  'type',
                  'author',
                  'contributor_list']
        read_only_fields = ['author', 'contributor_list']


class ProjectSerializerSelector:
    """Import container for the view and it's get_serializer method"""
    list = ProjectListSerializer
    detail = ProjectDetailSerializer


class IssueListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id',
                                            read_only=True)
    assignee_email = serializers.EmailField(source='assignee_user_id',required=False)
    tag = ChoiceField(choices=Issue.Tag.choices)
    priority = ChoiceField(choices=Issue.Priority.choices)
    status = ChoiceField(choices=Issue.Status.choices)

    class Meta:
        model = Issue
        fields = ['id',
                  'title',
                  'description',
                  'tag',
                  'priority',
                  'status',
                  'assignee_email',
                  'project_id',
                  'author']
        read_only_fields = ['project_id', 'author']


class IssueDetailSerializer(IssueListSerializer):
    class Meta:
        model = Issue
        fields = ['id',
                  'title',
                  'description',
                  'tag',
                  'priority',
                  'status',
                  'assignee_email',
                  'project_id',
                  'author',
                  'created_time']
        read_only_fields = ['project_id', 'author', 'created_time']


class IssueSerializerSelector:
    """Import container for the view and it's get_serializer method"""
    list = IssueListSerializer
    detail = IssueDetailSerializer


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id',
                  'description',
                  'project_id',
                  'issue_id',
                  'author']
        read_only_fields = ['project_id', 'issue_id', 'author']


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id', read_only=True)

    class Meta:
        model = Comment
        fields =  ['comment_id',
                   'description',
                   'project_id',
                   'issue_id',
                   'author',
                   'created_time']
        read_only_fields = ['project_id', 'issue_id', 'author', 'created_time']


class CommentSerializerSelector:
    """Import container for the view and it's get_serializer method"""
    list = CommentListSerializer
    detail = CommentDetailSerializer
