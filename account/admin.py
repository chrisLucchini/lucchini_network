from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'username', 'accepted']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name',
                           'password', 'accepted', 'is_superuser',
                           'is_staff', 'birth_date', 'location')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password',
                       'is_superuser', 'is_staff', 'accepted')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)