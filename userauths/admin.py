from django.contrib import admin
from userauths.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']
    pass

admin.site.register(model_or_iterable=User, admin_class=UserAdmin)