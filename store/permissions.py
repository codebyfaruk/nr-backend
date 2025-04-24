from rest_framework.permissions import BasePermission


class IsStaffPermission(BasePermission):
    """
    Custom permission to check if the staff is allowed to access a specific method.
    Admin can perform all actions, but staff can only perform specific methods.
    """

    def has_permission(self, request, view):
        allow_staff = getattr(view, "allow_staff", False)
        # Check if the action is 'destroy' (delete), then allow only admin (superuser)
        if view.action == "destroy":
            # Admin (superuser) can delete
            if (
                request.user
                and request.user.is_authenticated
                and request.user.is_superuser
            ):
                return True
            return False  # Deny delete action to staff

        if request.user.is_superuser:
            return True

        # Admin can access everything
        if request.user and request.user.is_authenticated and request.user.is_admin:
            return True

        # If the 'allow_staff' is True and the user is staff, grant permission
        if allow_staff and request.user.is_authenticated and request.user.is_staff:
            return True

        return False
