from rest_framework.permissions import BasePermission, SAFE_METHODS
from.models import Contributor

"""Nesting is to be checked in serializer for create/write methods and in 
get_querryset for list
These 2 permissions are mandatory after login for all CRUD operations"""

class IsContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user.user_id
        obj_project_id = obj.get_project_id()
        querryset = Contributor.objects.filter(
                                               user_id=user_id,
                                               project_id=obj_project_id
                                               )
        return len(querryset) > 0


class IsAuthorOrReadOnly(BasePermission):
    """
    Object-level permission to only allow its owner to edit/delete an object.
    Assumes the model instance has an `author_user_id` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author_user_id == request.user.user_id

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author_user_id == request.user.user_id
