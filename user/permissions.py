from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsRecruiter(permissions.BasePermission):
    message = {'message': 'You need recruiter privileges to perform this action'}
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
    
    def handle_no_permission(self, request):
        raise PermissionDenied({'message': self.message})

class IsSeeker(permissions.BasePermission):
    message = {'message': 'You need seeker privileges to perform this action'}
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff