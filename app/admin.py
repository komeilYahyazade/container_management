from django.contrib import admin
from .models import App, Container


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    pass


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    pass
