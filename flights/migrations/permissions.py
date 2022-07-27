import datetime
from rest_framework.permissions import BasePermission

class HasAuthority(BasePermission):
    message ='you are not authorized'
    def has_object_permission(self, request, view, obj):
        return request.user==obj.owner or request.user.is_staff
    
class IsNotTooSoon(BasePermission):
    message= "too early to make any changes"
    def has_object_permission(self, request, view, obj):
       
        return obj.date>= datetime.date.today()+ 3
    