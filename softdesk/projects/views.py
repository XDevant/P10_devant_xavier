from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from projects.models import Project, Issue, Comment
from projects.serializer import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
 
    def get_queryset(self):
        return Project.objects.all()