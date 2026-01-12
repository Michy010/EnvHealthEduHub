from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login
from django.db import IntegrityError
from django.http import JsonResponse
from mainApp . models import Education
import json

User = get_user_model()

# Create your views here.
def register_view (request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        education_level = request.POST.get('education')
        institution = request.POST.get('institution')


        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success':False,
                'message':'The email already exist.',
            }, status=409)
        else:
            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password
            )

            Education.objects.create(
                user = user,
                education_level = education_level,
                institution = institution

            )
            
            return JsonResponse({
                'success': True,
                'message': 'Your account has been created successful!'
            }, status=201)
        
    return render (request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({
                'success': False,
                'message': 'Email and password are required'
            }, status=400)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful'
            }, status=200)

        else:
            return JsonResponse({
                'success': False,
                'message': 'Incorrect email or password'
            }, status=400)

    return render(request, 'accounts/login.html')

def profile_edit(request, user_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        user_id = data.get('userId')

        print(first_name)
        print(last_name)
        print(email)
        print(user_id)

        # user instance which is editing the information
        user = User.objects.get(id=user_id)

        if first_name:
            user.first_name = first_name
            user.save()
            return JsonResponse({
                'message': 'First name updated'
            })
        if last_name:
            user.last_name = last_name
            user.save()
            return JsonResponse({
                'message': 'Last name updated'
            })
        if email:
            user.email = email
            user.save()
            return JsonResponse({
                'message': 'Email updated'
            })

    return render (request, 'mainApp/profile.html')