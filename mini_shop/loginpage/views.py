from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
# def login_page(request):
#     return render(request, 'loginpage/register.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return render(request, template_name="loginpage/succesful_login.html", context=request.GET.get('next'))
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request, template_name="loginpage/register.html",
                      context={"form_errors": form.errors, "register_form": form})
    form = NewUserForm()
    return render(request=request, template_name="loginpage/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return render(request, template_name="loginpage/succesful_login.html")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="loginpage/login.html", context={"login_form": form})
