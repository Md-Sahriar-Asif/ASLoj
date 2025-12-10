from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Problem, TestInput, TestOutput, Example, Submission, Contest, Discussion, Comment, Group, GroupInvitation, ContestRegistration, ContestSubmission


class UserAdmin(BaseUserAdmin):
    # Fields to display in the user list
    list_display = ('email', 'full_name', 'university_id', 'phone', 'points', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name', 'university_id', 'phone', 'points')
    ordering = ('email',)

    # Fields for user detail/edit page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'university_id', 'phone', 'points')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fields for creating new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'university_id', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('last_login',)


# Register the User model with the custom admin
admin.site.register(User, UserAdmin)
admin.site.register(Problem)
admin.site.register(TestInput)
admin.site.register(TestOutput)
admin.site.register(Example)
admin.site.register(Submission)
admin.site.register(Discussion)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(GroupInvitation)
admin.site.register(Contest)
admin.site.register(ContestRegistration)
admin.site.register(ContestSubmission)

