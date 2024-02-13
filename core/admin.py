from django.contrib import admin
from .models import Person,Anon,Anon_Response
# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    list_display=['first_name','email','admirer','response']
    
admin.site.register(Person,PersonAdmin)
admin.site.register(Anon)

class ResAdmin(admin.ModelAdmin):
    list_display=['user','response']
    
admin.site.register(Anon_Response,ResAdmin)