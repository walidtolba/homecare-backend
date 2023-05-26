from django.contrib import admin
from .models import User, Profile, VerificationCode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
    fields = ['email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_superuser', 'profile']
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
    # def has_change_permission(self, request, obj=None):
    #     return False