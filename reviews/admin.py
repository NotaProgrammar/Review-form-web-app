from django.contrib import admin

from reviews.models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name','price','rating')