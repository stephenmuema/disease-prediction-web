# Register your models here.
from django.contrib import admin

# the module name is app_name.models
from accounts.models import User, Profile


# username = models.CharField(max_length=20)
#     email = models.EmailField(max_length=255, unique=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     user_status = models.CharField(max_length=20, null=False, default="active")
#     timestamp = models.DateTimeField(auto_now_add=True)
#     phone_number = models.CharField(unique=True, null=True, blank=True, max_length=20)
#     user_type = models.CharField(default="customer", max_length=20)
#     email_confirmed = models.BooleanField(default=False)
#     location = models.CharField(max_length=30)

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'is_admin', 'is_staff', 'user_status',
        'user_type',
        'email_confirmed',)
    search_fields = ('first_name', 'last_name', 'email', 'user_type')


class ProfileAdmin(admin.ModelAdmin):
    #  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    #     address = models.CharField(max_length=200,blank=True,null=True)
    #     alternative_phone_number = models.CharField(null=True, blank=True, max_length=20)
    #     mobile_money_phone_number = models.CharField(null=True, blank=True, max_length=20)
    #     location = models.CharField(max_length=32)
    list_display = [
        'user', 'address'
    ]
    search_fields = [
        'address'
    ]


# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
