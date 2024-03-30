from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        return formfield

# Register the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Campaigns)
class Campaigns(admin.ModelAdmin):
    list_display = ('user','campaign_name','delivery_date','memo')
    list_filter = ('delivery_date','user')
    search_fields = ('campaign_name','user__email')


@admin.register(Orders)
class Orders(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)


from social_django.models import Nonce,UserSocialAuth,Association
from social_django.admin import Nonce,UserSocialAuth,Association
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Association)


# ----------Admin Customization------------
admin.site.site_header = "Coupoun True Effect Admin"
admin.site.site_title = "Coupoun True Effect"
admin.site.index_title = "Coupoun True Effect"
admin.site.unregister(Group)