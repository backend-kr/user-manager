from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.contrib.auth.admin import UserAdmin

from api.bases.users.models import User, Profile, Image

class UserProfileInline(admin.StackedInline):
    model = Profile
    raw_id_fields = ('avatar',)
    can_delete = False


class UserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions', 'site')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'site'),
        }),
    )

    list_filter = ('is_staff', 'is_active', 'groups', 'date_joined', 'site')
    list_display = ('email', 'is_staff', 'date_joined', 'site')
    search_fields = ('id', 'email', 'profile__name', 'profile__phone')
    ordering = ('email',)
    inlines = [UserProfileInline, ]

    def name(self, instance):
        return instance.profile.name

    def has_contract(self, instance):
        return instance.contract_set.filter(is_canceled=False).exists()

    def is_ordered(self, instance):
        return instance.orders.all().exists()

    name.admin_order_field = "profile__name"
    has_contract.boolean = True
    is_ordered.boolean = True

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'birth_date')
    search_fields = ('user__email', 'name', 'phone')
    raw_id_fields = ('user', 'avatar')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ('file', 'avatar__name', 'avatar__user__email')
    list_display = ('id', 'file', 'width', 'height')

admin.site.register(User, UserAdmin)
admin.site.register(Profile, UserProfileAdmin)


