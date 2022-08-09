from django.contrib import admin
from nba_app.models import *


# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "retire_year"]
    list_display_links = ["name"]

    def __str__(self):
        return f"{self.name}"


admin.site.register(Predict)
admin.site.register(Image)
