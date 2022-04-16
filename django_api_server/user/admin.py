from django.contrib import admin

from user.models import User

admin.site.site_title = "Django Api Server Template"
admin.site.site_header = "Django Api Server Template"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display_links = ('username',)
    fields = ('username', 'is_staff', 'is_active', 'is_superuser')
    list_display = ('username', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('id', 'username')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(is_active=True)
