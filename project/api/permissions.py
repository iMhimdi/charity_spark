from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes an owner field that can be configured via owner_field attribute.
    """
    owner_field = 'creator'  # Default owner field
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Get the owner field from the view if specified, otherwise use default
        owner_field = getattr(view, 'owner_field', self.owner_field)
        
        # Try to get the owner, return False if field doesn't exist
        try:
            owner = getattr(obj, owner_field)
            return owner == request.user
        except AttributeError:
            return False