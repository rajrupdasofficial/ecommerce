from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_admin', 'is_active',)
    list_filter = ('is_admin', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',)
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
