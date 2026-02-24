from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrAdmin(BasePermission):
    """
    Allow access only to staff or admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["staff", "admin"]
        )


class IsOwnerOrStaff(BasePermission):
    """
    Owner can access their reservation.
    Staff/admin can access all.
    """

    def has_object_permission(self, request, view, obj):

        # Staff/admin can access everything
        if request.user.role in ["staff", "admin"]:
            return True

        # Owner can access their own reservation
        return obj.user == request.user


class ReadOnlyOrStaff(BasePermission):
    """
    Anyone can read.
    Only staff/admin can modify.
    """

    def has_permission(self, request, view):

        # Read allowed for everyone
        if request.method in SAFE_METHODS:
            return True

        # Write allowed only for staff/admin
        return (
            request.user.is_authenticated
            and request.user.role in ["staff", "admin"]
        )