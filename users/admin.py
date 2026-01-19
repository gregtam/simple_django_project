from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # This adds 'uuid' to the columns in the list view
    list_display = ('uuid', 'username', 'first_name', 'last_name')

    # Optional: If you want to see the uuid inside the "Change User" form:
    readonly_fields = ('uuid',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('uuid',)}),
    )

admin.site.register(User, CustomUserAdmin)