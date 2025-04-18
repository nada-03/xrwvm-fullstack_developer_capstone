import logging
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


def login_user(request):
    """Handle sign in request"""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    """Handle sign out request"""
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


def authenticate_user(request):
    """Handle sign up request"""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("%s is a new user", username)

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)

    data = {"userName": username, "error": "Already Registered"}
    return JsonResponse(data)


def get_dealerships(request):
    """Get dealership data from cloud function"""
    if request.method == "GET":
        url = "https://api.example.com/dealerships"
        dealerships = get_request(url)
        return JsonResponse(dealerships, safe=False)


def get_dealer_details(request, dealer_id):
    """Get dealer reviews and sentiment"""
    if request.method == "GET":
        url = f"https://api.example.com/reviews?dealerId={dealer_id}"
        reviews = get_request(url)
        for review in reviews:
            sentiment = analyze_review_sentiments(review["review"])
            review["sentiment"] = sentiment
        return JsonResponse(reviews, safe=False)


def add_review(request, dealer_id):
    """Submit review to cloud function"""
    if request.method == "POST":
        data = json.loads(request.body)
        payload = {
            "review": data["review"],
            "name": data["name"],
            "dealership": dealer_id,
            "purchase": data.get("purchase", False),
            "purchase_date": data.get("purchase_date", ""),
            "car_make": data.get("car_make", ""),
            "car_model": data.get("car_model", ""),
            "car_year": data.get("car_year", ""),
        }
        url = "https://api.example.com/postreview"
        response = post_review(url, payload)
        return JsonResponse(response)
