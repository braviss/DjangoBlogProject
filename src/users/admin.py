from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from allauth.account.models import EmailAddress


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email',  'date_joined', 'is_email_verified')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
    inlines = [
        EmailAddressInline,
    ]
    save_on_top = True

    @admin.display(boolean=True)
    def is_email_verified(self, obj):
        return EmailAddress.objects.filter(user=obj, verified=True).exists()
