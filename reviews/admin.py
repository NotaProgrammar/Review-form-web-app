from django.contrib import admin
from django.contrib.auth.models import User, Group

# Import project models
from reviews.models import Food, ServiceReview, ReviewItem, Review


from django.contrib import admin

# Customizing admin panel titles
admin.site.site_header = "Restaurant Feedback Admin"
admin.site.site_title = "Restaurant Admin Portal"
admin.site.index_title = "Welcome to the Review Dashboard"

# Remove default authentication models from admin panel
admin.site.unregister(Group)
admin.site.unregister(User)



# Register Food model in admin panel
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    # Columns displayed in the food list page
    list_display = ('name','price','rating','purchase_count')


# Inline section to display ServiceReview inside Review page
class ServiceReviewInline(admin.StackedInline):
    model = ServiceReview
    extra = 0
    can_delete = False

    # Fields to display in the inline form
    fields = ["first_time", "duration", "service_quality", "review_text"]

    # Make fields read-only (admin cannot edit them)
    readonly_fields = ["first_time", "duration", "service_quality", "review_text"]

    # Prevent adding ServiceReview from admin
    def has_add_permission(self, request, obj=None):
        return False


# Inline table to display ReviewItem objects inside Review page
class ReviewItemInline(admin.TabularInline):
    model = ReviewItem
    extra = 0
    can_delete = False
    show_change_link = False

    # Fields displayed in the inline table
    fields = [
        "food",
        "quantity",
        "first_time",
        "food_quality",
        "food_size",
        "food_price",
        "review_text"
    ]

    # Make fields read-only
    readonly_fields = [
        "food",
        "quantity",
        "first_time",
        "food_quality",
        "food_size",
        "food_price",
        "review_text"
    ]

    # Prevent adding new ReviewItem from admin
    def has_add_permission(self, request, obj=None):
        return False


# Register Review model in admin panel
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Order reviews by newest first
    ordering = ["-created_at"]

    # Columns shown in the review list page
    list_display = ['id', 'customer', 'created_at']

    # Attach related models inside Review page
    inlines = [ServiceReviewInline, ReviewItemInline]

    # Filter sidebar
    list_filter = ['created_at']

    # Enable searching by customer information
    search_fields = [
        'customer__first_name',
        'customer__last_name',
        'customer__phone_number'
    ]

    # Prevent adding Review manually from admin
    def has_add_permission(self, request):
        return False

    # Prevent editing Review from admin
    def has_change_permission(self, request, obj=None):
        return False
