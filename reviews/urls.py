from django.urls import path

from reviews import views

urlpatterns = [
    path('entry/', views.entry),
    path('customer_details/',views.customer_details_preprocess),
    path('foods_page/', views.foods_page_preprocess),
    path('service_form/', views.service_form_preprocess),
    path('food_form/', views.food_form_preprocess),
    path('next_food_page/', views.next_food_page_preprocess),
]