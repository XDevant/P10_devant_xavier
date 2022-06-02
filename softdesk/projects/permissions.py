from rest_framework.permissions import BasePermission, SAFE_METHODS
from.models import Contributor


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        try:
            Contributor.objects.get(
                                       user_id=request.user.user_id,
                                       project_id=view.kwargs['projects_pk']
                                       )
            return True
        except Exception:
            return False


class IsAuthorOrReadOnly(BasePermission):
    """
    Object-level permission to only allow its owner to edit/delete an object.
    Assumes the model instance has an `author_user_id` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user_id == request.user
