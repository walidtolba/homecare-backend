from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    """
    Allows access only to Pateints.
    """

    def has_permission(self, request, view):
        return bool(request.user.profile.title == 'P')

class IsMedic(BasePermission):
    """
    Allows access only to Medics.
    """

    def has_permission(self, request, view):
        return bool(request.user.profile.title == 'M')
    
class IsNurse(BasePermission):
    """
    Allows access only to Nurses.
    """

    def has_permission(self, request, view):
        return bool(request.user.profile.title == 'N')
    
class IsPharmasist(BasePermission):
    """
    Allows access only to Pharmasists.
    """

    def has_permission(self, request, view):
        return bool(request.user.profile.title == 'F')
    
class IsDriver(BasePermission):
    """
    Allows access only to Driver.
    """

    def has_permission(self, request, view):
        return bool(request.user.profile.title == 'D')
  
  
class IsSupport(BasePermission):
    """
    Allows access only to Pharmasists.
    """

    def has_permission(self, request, view):
        return bool(request.user.profile.title == 'S')