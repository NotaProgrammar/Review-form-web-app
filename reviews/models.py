from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    purchase_count = models.IntegerField(default=0)
    phone_number = models.CharField(null=True,max_length=11,blank=True)

class Food(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(default=0)
    rating = models.IntegerField(default=0,blank=True)


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)



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
        (GOOD, 'Good'),
        (MEDIUM, 'Medium'),
        (BAD, 'Bad'),
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


    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    first_time = models.BooleanField(null=False, default=True)
    food_quality = models.CharField(choices=FOOD_QUALITY_CHOICES, max_length=1, default=MEDIUM)
    food_size = models.CharField(choices=FOOD_SIZE_CHOICES, max_length=1, default=ADEQUATE)
    food_price = models.CharField(choices=FOOD_PRICE_CHOICES, max_length=1, default=WELL_PRICED)
    review_text = models.TextField()

    class Meta:
        constraints = [
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

    review = models.OneToOneField(Review, on_delete=models.CASCADE, primary_key=True)
    first_time = models.BooleanField(null=False, default=True)
    duration = models.CharField(choices=DURATION_CHOICES, max_length=1, default=EXPECTED)
    service_quality = models.CharField(choices=SERVICE_QUALITY_CHOICES, max_length=1, default=MEDIUM)
    review_text = models.TextField(blank=True, null=True)