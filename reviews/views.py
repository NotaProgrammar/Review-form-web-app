from django.db.models import F
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect

from reviews.models import Customer, Food, Review, ServiceReview, ReviewItem


def entry(request):
    request.session["entry_allowed"] = True
    return render(request,'entry.html')


def customer_details_preprocess(request):
    if not request.session.get("entry_allowed"):
        return redirect("/form/entry/")

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
    selected_foods = request.POST.getlist("foods")
    request.session["selected_foods"] = selected_foods
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

    ServiceReview.objects.create(review = current_review,first_time=first_time,duration=duration,service_quality=service_quality, review_text=review_text)

    selected_foods = request.session.get("selected_foods", [])
    if selected_foods:
        current_food = selected_foods.pop(0)
        # request.session["current"]
        request.session["selected_foods"] = selected_foods
        # return render(request, "food_form.html", {"food": current_food})
        return HttpResponse(current_food.name)

    return render(request, "final.html")

def next_food_page_preprocess(request):
    current_review = request.session["current_review"]
    first_time = request.POST.get("first_time")
    quantity = request.POST.get("quantity")
    review_text = request.POST.get("review_text")
    food_quality = request.POST.get("food_quality")
    food_size = request.POST.get("food_size")
    food_price = request.POST.get("food_price")

    # review_item = ReviewItem.objects.create(request=current_review,
    #                                         first_time=first_time,
    #                                         quantity=quantity,
    #                                         review_text= review_text,
    #                                         food_quality=food_quality,
    #                                         food_size=food_size,
    #                                         food_price=food_price)
    #

    return HttpResponseForbidden()

