from rest_framework.serializers import ModelSerializer, SerializerMethodField
from projects.models import Project, Issue, Comment


class ProjectListSerializer(ModelSerializer):
    contributors = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'contributors']

    def get_contributors(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProjectListSerializer(queryset, many=True)
        return serializer.data

class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author', 'contributors', 'issues']


class ProjectSerializerSelector:
    list = ProjectListSerializer
    retrieve = ProjectDetailSerializer


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