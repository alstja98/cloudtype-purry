from django.contrib import admin
from .models import User, Images, Prompt

# Register your models here.
class userAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'id', 'update_time')
admin.site.register(User, userAdmin)

class imagesAdmin(admin.ModelAdmin):
    list_display = ('update_time','user_id','type','path')
admin.site.register(Images, imagesAdmin)

