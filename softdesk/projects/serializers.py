from rest_framework import serializers
from projects.models import Project, Issue, Comment, Contributor
from authentication.models import User


class ChoiceField(serializers.ChoiceField):
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
    user_id = serializers.StringRelatedField()

    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'role']
        read_only_fields = ['user_id']


class ContributorCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.EmailField(max_length=140)

    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'role']

class ContributorDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField()

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only_fields = ['user_id', 'project_id', 'permission', 'role']


class ContributorSerializerSelector:
    list = ContributorListSerializer
    detail = ContributorDetailSerializer
    create = ContributorCreateSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id', read_only=True)
    type = ChoiceField(choices=Project.Type.choices)

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author']
        read_only_fields = ['author']
        

class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id', read_only=True)
    contributor_list = ContributorListSerializer(many=True, read_only=True)
    type = ChoiceField(choices=Project.Type.choices)

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
    list = ProjectListSerializer
    detail = ProjectDetailSerializer


class IssueListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id', read_only=True)
    assignee_user_id = ContributorFilteredPKRF(queryset=User.objects.all(), required=False)
    tag = ChoiceField(choices=Issue.Tag.choices)
    priority = ChoiceField(choices=Issue.Priority.choices)
    status = ChoiceField(choices=Issue.Status.choices)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'assignee_user_id', 'project_id', 'author']
        read_only_fields = ['project_id', 'author']


class IssueDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id', read_only=True)
    assignee_user_id = ContributorFilteredPKRF(queryset=User.objects.all(), required=False)
    tag = ChoiceField(choices=Issue.Tag.choices)
    priority = ChoiceField(choices=Issue.Priority.choices)
    status = ChoiceField(choices=Issue.Status.choices)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'assignee_user_id', 'project_id', 'author', 'created_time']
        read_only_fields = ['project_id', 'author', 'created_time']


class IssueSerializerSelector:
    list = IssueListSerializer
    detail = IssueDetailSerializer


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment_id', 'description', 'project_id', 'issue_id', 'author']
        read_only_fields = ['project_id', 'issue_id', 'author']


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author_user_id', read_only=True)

    class Meta:
        model = Comment
        fields =  ['comment_id', 'description', 'project_id', 'issue_id', 'author', 'created_time']
        read_only_fields = ['project_id', 'issue_id', 'author', 'created_time']


class CommentSerializerSelector:
    list = CommentListSerializer
    detail = CommentDetailSerializer
