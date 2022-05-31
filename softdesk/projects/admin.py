from django.contrib import admin
from projects.models import Project, Contributor, Issue, Comment


admin.site.register([Project, Contributor, Issue, Comment])
