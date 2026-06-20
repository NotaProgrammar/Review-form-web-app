from django.db.models import F
from django.shortcuts import render

from reviews.models import Customer, Food, Review, ServiceReview, ReviewItem


def entry(request):
    return render(request,'entry.html')


def customer_details_preprocess(request):
    return render(request, "customer_details.html")

def foods_page_preprocess(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone = request.POST.get("phone")

    customer, created = Customer.objects.get_or_create(
        phone_number=phone,
        defaults={'first_name': first_name, 'last_name': last_name}
    )

    Customer.objects.filter(pk=customer.pk).update(
        purchase_count=F("purchase_count") + 1
    )

    foods_query = Food.objects.all()
    current_review = Review.objects.create(customer=customer)
    request.session['current_review'] = current_review.id

    return render(request, "foods_page.html", {"foods": list(foods_query)})

def service_form_preprocess(request):
    selected_food_ids = request.POST.getlist("foods")

    if not selected_food_ids:
        return render(request, "foods_page.html", {
            "foods": Food.objects.all(),
            "error": "لطفاً حداقل یک غذا انتخاب کنید."
        })

    selected_foods = Food.objects.filter(id__in=selected_food_ids)
    foods_data = list(
        selected_foods.values("id", "name")
    )
    request.session["selected_foods"] = foods_data
    return render (request, "service_form.html")

def food_form_preprocess(request):
    current_review = Review.objects.get(pk=request.session["current_review"])
    purchase_count = Customer.objects.get(pk=current_review.customer.id).purchase_count

    first_time = False
    if purchase_count == 1:
        first_time = True
    duration = request.POST.get("duration")
    service_quality = request.POST.get("service_quality")
    review_text = request.POST.get("review_text")

    ServiceReview.objects.update_or_create(review = current_review,
                                           first_time=first_time,
                                           duration=duration,
                                           service_quality=service_quality,
                                           review_text=review_text
                                           )

    selected_foods = request.session.get("selected_foods", [])
    current_food = selected_foods.pop(0)
    request.session["selected_foods"] = selected_foods

    return render(request, "food_form.html", {"food_name": current_food['name'], "food_id": current_food['id']})


def next_food_page_preprocess(request):
    current_review = request.session["current_review"]
    food_id = request.POST.get("food_id")
    first_time = request.POST.get("first_time") is "on"
    quantity = int(request.POST.get("quantity", 1))
    review_text = request.POST.get("review_text")
    food_quality = request.POST.get("food_quality")
    food_size = request.POST.get("food_size")
    food_price = request.POST.get("food_price")

    review_item = ReviewItem.objects.create(review_id=current_review,
                                            first_time=first_time,
                                            quantity=quantity,
                                            review_text= review_text,
                                            food_quality=food_quality,
                                            food_size=food_size,
                                            food_price=food_price,
                                            food_id = food_id,)

    score = scoring(food_size,food_quality,food_price)
    Food.objects.filter(id=food_id).update(
        rating=(F("rating") * F("purchase_count") + quantity * score) / (F("purchase_count") + quantity),
        purchase_count=F("purchase_count") + quantity
    )

    selected_foods = request.session.get("selected_foods", [])
    if selected_foods:
        current_food = selected_foods.pop(0)
        request.session["selected_foods"] = selected_foods
        return render(request, "food_form.html", {"food_name": current_food['name'], "food_id": current_food['id']})

    return render(request, "final.html")



def scoring(size,quality,price):
    QUALITY_SCORE = {
        "E": 5,
        "G": 4,
        "M": 3,
        "B": 2,
        "T": 1,
    }

    SIZE_SCORE = {
        "G": 5,
        "M": 3,
        "B": 1,
    }

    PRICE_SCORE = {
        "I": 5,
        "W": 3,
        "E": 1,
    }

    quality_score = QUALITY_SCORE.get(quality, 0)
    size_score = SIZE_SCORE.get(size, 0)
    price_score = PRICE_SCORE.get(price, 0)

    score = (quality_score + size_score + price_score)/3
    return score
