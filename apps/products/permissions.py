from rest_framework import permissions


class IsAdminUser(permissions.IsAdminUser):

    def has_permission(self, request, view):
        return True

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return obj.author == request.user