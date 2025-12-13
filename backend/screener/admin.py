from django.contrib import admin
from .models import Screener

# Register your models here.
class ScreenerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')

admin.site.register(Screener, ScreenerAdmin)