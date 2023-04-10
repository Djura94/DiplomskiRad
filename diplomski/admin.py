from django.contrib import admin

from .models import Course, SubscribedUsers

class SubscirbedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name','created_date')


admin.site.register(Course)
admin.site.register(SubscribedUsers,SubscirbedUsersAdmin)