from rest_framework.permissions import BasePermission


class IsCashierUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 0)


class IsBaristaUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.role > 1)


class IsManagerUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.role > 2)


class IsOwnerUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 3 and request.user.is_superuser)
