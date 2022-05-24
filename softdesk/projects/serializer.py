from rest_framework.serializers import ModelSerializer
from projects.models import Project, Issue, Comment


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = []

class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = []

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = []
