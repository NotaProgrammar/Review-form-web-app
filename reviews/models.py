from django.db import models


class Customer(models.Model):
    # Stores basic customer information
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    purchase_count = models.IntegerField(default=0)
    phone_number = models.CharField(null=True,max_length=11,blank=True)

    def __str__(self):
        return self.phone_number



class Food(models.Model):
    # Stores food details and overall rating data
    name = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(default=0)
    rating = models.DecimalField(default=0,null=True,blank=True,max_digits=3,decimal_places=2)
    purchase_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "غذا"
        verbose_name_plural = "غذاها"


class Review(models.Model):
    # Represents one full review submitted by a customer
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return "نظر سنجی شماره " + self.id.__str__()

    class Meta:
        verbose_name = "نظرسنجی"
        verbose_name_plural = "نظرسنجی‌ها"



class ReviewItem(models.Model):
    #food quality choices
    EXCELLENT = 'E'
    GOOD = 'G'
    MEDIUM = 'M'
    BAD = 'B'
    TERRIBLE = 'T'

    FOOD_QUALITY_CHOICES = [
        (EXCELLENT, 'Excellent'),
        (GOOD, 'Good'),
        (MEDIUM, 'Medium'),
        (BAD, 'Bad'),
        (TERRIBLE, 'Terrible'),
    ]

    #food size choices
    GENEROUS = 'G'
    ADEQUATE = 'A'
    SMALL = 'S'

    FOOD_SIZE_CHOICES = [
        (GENEROUS, 'Generous'),
        (ADEQUATE, 'Adequate'),
        (SMALL, 'Small'),
    ]

    #food price choices
    INEXPENSIVE = 'I'
    WELL_PRICED = 'W'
    EXPENSIVE = 'E'
    FOOD_PRICE_CHOICES = [
        (INEXPENSIVE, 'Inexpensive'),
        (WELL_PRICED, 'Well priced'),
        (EXPENSIVE, 'Expensive'),
    ]

    # Stores feedback for one specific food in a review
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    first_time = models.BooleanField(null=False, default=True)
    food_quality = models.CharField(choices=FOOD_QUALITY_CHOICES, max_length=1, default=MEDIUM,blank=True)
    food_size = models.CharField(choices=FOOD_SIZE_CHOICES, max_length=1, default=ADEQUATE,blank=True)
    food_price = models.CharField(choices=FOOD_PRICE_CHOICES, max_length=1, default=WELL_PRICED,blank=True)
    review_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.food.name

    class Meta:
        constraints = [
            # Prevents duplicate food reviews within the same review
            models.UniqueConstraint(
                fields=['review', 'food'],
                name='composite_id',
            )
        ]


class ServiceReview(models.Model):
    #duration choices
    SLOW = 'S'
    EXPECTED = 'E'
    FAST = 'F'
    DURATION_CHOICES = [
        (SLOW, 'Slower than expected'),
        (EXPECTED, 'As expected'),
        (FAST, 'Faster than expected'),
    ]

    #service quality choices
    EXCELLENT = 'E'
    GOOD = 'G'
    MEDIUM = 'M'
    BAD = 'B'
    TERRIBLE = 'T'

    SERVICE_QUALITY_CHOICES = [
        (EXCELLENT, 'Excellent'),
        (GOOD, 'Good'),
        (MEDIUM, 'Medium'),
        (BAD, 'Bad'),
        (TERRIBLE, 'Terrible'),
    ]

    # Stores the overall service feedback for a review
    review = models.OneToOneField(Review, on_delete=models.CASCADE, primary_key=True)
    first_time = models.BooleanField(null=False, default=True)
    duration = models.CharField(choices=DURATION_CHOICES, max_length=1, default=EXPECTED, null=True)
    service_quality = models.CharField(choices=SERVICE_QUALITY_CHOICES, max_length=1, default=MEDIUM,null=True)
    review_text = models.TextField(blank=True, null=True)
