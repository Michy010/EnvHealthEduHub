from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomeUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('first_name', 'last_name', 'email', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            ),
        }),
    )

    search_fields = ('email', 'first_name')
    ordering = ['email',]