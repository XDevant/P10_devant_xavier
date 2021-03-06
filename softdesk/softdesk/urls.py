"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from projects.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet, basename='project')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
project_router.register(r'contributors', ContributorViewSet, basename='contributors')
project_router.register(r'issues', IssueViewSet, basename='issues')

issue_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='issues')
issue_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path(r'', include(router.urls)),
    path(r'', include(project_router.urls)),
    path(r'', include(issue_router.urls))
]
