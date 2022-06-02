from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField, RelatedField, PrimaryKeyRelatedField
from projects.models import Project, Issue, Comment, Contributor
from authentication.models import User


class UserFilteredPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)


class ContributorFilteredPKRF(PrimaryKeyRelatedField):
    def get_queryset(self):
        view = self.context.get('view', None)
        queryset = super(ContributorFilteredPKRF, self).get_queryset()
        if not view or not queryset:
            return None
        project_id = view.kwargs['projects_pk']
        queryset = queryset.filter(project_contributors__project_id=project_id)
        return queryset


class ContributorListSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id', 'permission', 'role']
        read_only_fields = ['user_id', 'project_id', 'permission']


class ContributorSerializerSelector:
    list = ContributorListSerializer
    detail = ContributorListSerializer


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
    assignee_user_id = ContributorFilteredPKRF(queryset=User.objects.all(), required=False)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'assignee_user_id', 'project_id', 'author_user_id']
        read_only_fields = ['project_id', 'author_user_id']


class IssueDetailSerializer(ModelSerializer):
    assignee_user_id = ContributorFilteredPKRF(queryset=User.objects.all(), required=False)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['project_id', 'author_user_id', 'created_time']


class IssueSerializerSelector:
    list = IssueListSerializer
    detail = IssueDetailSerializer


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_time']
        read_only_fields = ['project_id', 'issue_id', 'author_user_id']


class CommentDetailSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['project_id', 'issue_id', 'author_user_id', 'created_time']


class CommentSerializerSelector:
    list = CommentListSerializer
    detail = CommentDetailSerializer
