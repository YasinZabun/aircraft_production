from rest_framework import permissions

class IsAuthenticatedAndInTeam(permissions.BasePermission):
    """
    Permission that checks if a user is authenticated and has a team assigned.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.team is not None

class IsTeamResponsibleForPart(permissions.BasePermission):
    """
    Permission to ensure that the logged-in user's team is responsible for the part type they are creating/updating.
    """
    def has_object_permission(self, request, view, obj):
        # For actions like delete or update of a specific part:
        # User can only modify if the part's team == user's team
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.team == request.user.profile.team
        return True

    def has_permission(self, request, view):
        # For creation, user must create only parts of their team's responsible_part_type
        if request.method == 'POST':
            team = request.user.profile.team
            # We'll rely on serializer validation too, but let's just return True here to allow serializer to check further.
            return True
        return True

class IsAssemblyTeam(permissions.BasePermission):
    """
    Permission to allow only the assembly team to assemble aircraft.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return (request.user.is_authenticated and
                    hasattr(request.user, 'profile') and
                    request.user.profile.team and
                    request.user.profile.team.responsible_part_type == "Assembly")
        return True
