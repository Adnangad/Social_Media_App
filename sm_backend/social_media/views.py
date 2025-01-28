from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from uuid import uuid4
from django.contrib.auth.hashers import make_password, check_password



def say_hello(request):
    """Says returns a respons that says hello world"""
    return HttpResponse("Hello world")


@csrf_exempt
def sign_up(request):
    """Retrieves user credentials and adds them to the database"""
    if request.method == "POST":
        try:
            # Parse the data from the request body
            username = request.POST.get('name')
            email = request.POST.get('email')
            password = make_password(request.POST.get('password'))
            dob = request.POST.get('dob')
            location = request.POST.get('location')
            img = request.FILES.get('profile')

            # Validates required fields
            if not all([username, email, password, dob, location]):
                return JsonResponse({'error': "Missing required fields"}, status=400)
            
            person = People.objects.filter(email=email).exists()
            per2 = People.objects.filter(user_name=username).exists()

            if person or per2:
                return JsonResponse({'error': 'A user with the email/username already exists'}, status=403)

            # Saves the new user to the database
            if img:
                person = People.objects.create(
                    user_name=username,
                    email=email,
                    password=password,
                    date_of_birth=dob,
                    location=location,
                    profile_pic=img
                )
            else:
                person = People.objects.create(
                    user_name=username,
                    email=email,
                    password=password,
                    date_of_birth=dob,
                    location=location
                )

            token = uuid4()
            cache.set(f'auth_{token}', email, 86400)

            obj = model_to_dict(person)

            # Includes the profile_pic URL if it exists
            if person.profile_pic:
                obj['profile_pic'] = person.profile_pic.url

            return JsonResponse({"user": obj, "token": str(token)}, status=200)

        except json.JSONDecodeError:
            # Handles JSON parsing errors
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        except Exception as e:
            # Logs and handles unexpected errors
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    # Handles unsupported HTTP methods
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def login(request):
    """Handle user login and token generation."""
    try:
        # Parse JSON body
        data = json.loads(request.body.decode('utf-8'))
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"error": "Email and password are required"}, status=400)

        # Fetch user by email
        try:
            person = People.objects.get(email=email)
        except People.DoesNotExist:
            return JsonResponse({"error": "Invalid email/password"}, status=401)

        # Verify password
        if not check_password(password, person.password):
            return JsonResponse({"error": "Invalid email/password"}, status=401)

        # Generate and store token
        token = uuid4()
        cache.set(f"auth_{token}", email, 86400)  # Token expires in 1 day

        # Prepare response data (excluding sensitive fields like password)
        user_data = {
            "id": person.id,
            "user_name": person.user_name,
            "email": person.email,
            "date_of_birth": person.date_of_birth,
            "location": person.location,
            "profile_pic": person.profile_pic.url if person.profile_pic else None
        }

        return JsonResponse({"user": user_data, "token": str(token)}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)