from rest_framework import permissions

#custom permission for editors
class IsEditor(permissions.BasePermission):
    """
    Custom permission for editors
    """

    def has_permission(self, request, view):
        return request.user.is_editor