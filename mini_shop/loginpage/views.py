from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser


# Create your views here.
# def login_page(request):
#     return render(request, 'loginpage/register.html')


def register_request(request):
    if request.method == "GET":
        context = {"register_form": NewUserForm()}
        return render(request=request, template_name="loginpage/register.html", context=context)
    else:
        filled_form = NewUserForm(request.POST)
        if filled_form.is_valid():
            username = filled_form.cleaned_data.get('username')
            email = filled_form.cleaned_data.get('email')
            hashed_password = make_password(filled_form.cleaned_data.get('password1'))
            user = CustomUser(username=username, password=hashed_password, email=email)
            user.save()
            request.session['authorized'] = True
            return render(request=request, template_name="loginpage/succesful_login.html")
        else:
            return render(request, template_name="loginpage/register.html",
                          context={"form_errors": filled_form.errors, "register_form": filled_form})


# if request.method == "POST":
#     form = NewUserForm(request.POST)
#     if form.is_valid():
#         user = form.save()
#         login(request, user)
#         messages.success(request, "Registration successful.")
#         return render(request, template_name="loginpage/succesful_login.html",
#                       context={'previous_page': request.GET.get('next')})
#     messages.error(request, "Unsuccessful registration. Invalid information.")
#     return render(request, template_name="loginpage/register.html",
#                   context={"form_errors": form.errors, "register_form": form})
# form = NewUserForm()
# return render(request=request, template_name="loginpage/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request=request, template_name="loginpage/login.html", context={"login_form": form})
    else:
        filled_form = LoginForm(request.POST)
        if filled_form.is_valid():
            request.session['authorized'] = True
            response = render(request=request, template_name="loginpage/succesful_login.html")
            if filled_form.cleaned_data.get('remember_me'):
                response.set_cookie("login_info", f"{filled_form.cleaned_data.get('user_login')},"
                                                  f"{make_password(filled_form.cleaned_data.get('password'))}")
            return response
        else:
            return render(request, template_name="loginpage/login.html",
                          context={"form_errors": filled_form.errors, "login_form": filled_form})




    # if request.method == "POST":
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             messages.info(request, f"You are now logged in as {username}.")
    #             print(request.GET.get('next'))
    #             return render(request, template_name="loginpage/succesful_login.html",
    #                           context={'previous_page': request.GET.get('next')})
    #         else:
    #             messages.error(request, "Invalid username or password.")
    #     else:
    #         messages.error(request, "Invalid username or password.")
    # form = AuthenticationForm()
    # return render(request=request, template_name="loginpage/login.html", context={"login_form": form})


@login_required(login_url='/accounts/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'loginpage/change_password.html',
                          {'form_errors': form.errors, 'changepass_form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'loginpage/change_password.html', {'changepass_form': form})


# @login_required(login_url='/accounts/login')
def profile(request):
    print(request.profile.username)
    context = {'nickname': request.profile.username,
               'email': request.profile.email,
               'gender': 'Мужчина' if request.profile.gender == 'm' else 'Женщина',
               'firstname': request.profile.firstname,
               'lastname': request.profile.lastname}
    return render(request=request, template_name="loginpage/profile.html", context=context)


@login_required(login_url='/accounts/login')
def logout_view(request):
    logout(request)
    return redirect('/')
