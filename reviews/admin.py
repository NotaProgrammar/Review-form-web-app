from django.contrib import admin
from django.contrib.auth.models import User, Group

from reviews.models import Food, ServiceReview, ReviewItem, Review


from django.contrib import admin

admin.site.site_header = "Restaurant Feedback Admin"
admin.site.site_title = "Restaurant Admin Portal"
admin.site.index_title = "Welcome to the Review Dashboard"

admin.site.unregister(Group)
admin.site.unregister(User)



@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name','price','rating','purchase_count')


class ServiceReviewInline(admin.StackedInline):
    model = ServiceReview
    extra = 0
    can_delete = False

    fields = ["first_time", "duration", "service_quality", "review_text"]
    readonly_fields = ["first_time", "duration", "service_quality", "review_text"]

    def has_add_permission(self, request, obj=None):
        return False

class ReviewItemInline(admin.TabularInline):
    model = ReviewItem
    extra = 0
    can_delete = False

    fields = [
        "food",
        "quantity",
        "first_time",
        "food_quality",
        "food_size",
        "food_price",
        "review_text"
    ]

    readonly_fields = [
        "food",
        "quantity",
        "first_time",
        "food_quality",
        "food_size",
        "food_price",
        "review_text"
    ]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]

    list_display = ['id', 'customer', 'created_at']

    inlines = [ServiceReviewInline, ReviewItemInline]

    list_filter = ['created_at']
    search_fields = ['customer__name']

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False