from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone")

    def username(self, obj):
        return obj.user.get_full_name() or obj.user.username
    username.short_description = "Name"

    def email(self, obj):
        return obj.user.email
