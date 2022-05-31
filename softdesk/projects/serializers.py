from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField
from projects.models import Project, Issue, Comment


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id']
        read_only_fields = ['author_user_id']


class ProjectDetailSerializer(ModelSerializer):
    contributors = StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id', 'contributors']
        read_only_fields = ['author_user_id']


class ProjectSerializerSelector:
    list = ProjectListSerializer
    detail = ProjectDetailSerializer


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = []


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


class ContributorListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = []