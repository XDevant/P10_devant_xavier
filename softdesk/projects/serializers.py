from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField, RelatedField, PrimaryKeyRelatedField
from projects.models import Project, Issue, Comment, Contributor


class ContributorListSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id', 'permission', 'role']
        read_only_fields = ['user_id', 'project_id', 'permission']


class ProjectListSerializer(ModelSerializer):
    author_user_id = StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id']
        read_only_fields = ['author_user_id']


class ProjectDetailSerializer(ModelSerializer):
    contributor_list = ContributorListSerializer(many=True, read_only=True)
    author_user_id = StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id', 'contributor_list']
        read_only_fields = ['author_user_id', 'contributor_list']
        depth = 1


class ProjectSerializerSelector:
    list = ProjectListSerializer
    detail = ProjectDetailSerializer


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'project_id', 'status']
        read_only_fields = ['author_user_id', 'project_id']

class IssueDetailSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = []


class IssueSerializerSelector:
    list = IssueListSerializer
    retrieve = IssueDetailSerializer


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = []
