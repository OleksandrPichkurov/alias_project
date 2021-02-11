from django.contrib import admin
from .models import Alias
# Register your models here.

class Aliasdmin(admin.ModelAdmin):
    list_display = ['alias', 'target', 'start', 'end']


admin.site.register(Alias, Aliasdmin)