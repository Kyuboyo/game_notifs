from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout

from common.utils import sendResponse, responseSchema
import copy
# Create your views here.
class CreateProfile(APIView):
    def post(self, request):
        res = copy.deepcopy(responseSchema)
        data = {
                    "username"      : request.POST.get('username'),
                    "email"         : request.POST.get('email'),
                    "password1"     : request.POST.get('password1'), 
                    "password2"     : request.POST.get('password2')
                }
        form = SignUpForm(data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            UserProfile.objects.create(user=user, subscription=True)
            return redirect('/core/offers')
        else:
            res['status'] = "Failed"
            res['error_message'] = "Failed to Signup. Please check your details"
            return sendResponse(400, res)
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form':form})


class LoginView(APIView):

    authentication_classes  = []
    permission_classes      = []
    def post(self, request, format=None):
        res = copy.deepcopy(responseSchema)
        try:
            data = request.data
            username = data.get('username', None)
            password = data.get('password', None)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    return redirect("/core/offers")
                else:
                    res['status'] = "Failed"
                    res['error_message'] = "This account is not active"
                    return sendResponse(400, res)
            else:
                res['status'] = "Failed"
                res['error_message'] = "Invalid username or password"
                return sendResponse(400, res)

        except Exception as e:
            res['status'] = 'Failed'
            res['error_message'] = str(e)
            return sendResponse(500, res)

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})

class LogoutView(APIView):
    def get(self, request):
        res = copy.deepcopy(responseSchema)

        try:
            #check codewithharry for this (more to add)
            logout(request)
            res['status'] = "Success"
            res['message'] = "Logged out successfully"
            
            return redirect('/core/offers')
        except Exception as e:
            res['status'] = "Failed"
            res['error_message'] = str(e)
            return sendResponse(500, res)
