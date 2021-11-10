from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, ChangePassForm, ChangeProfileForm
from .models import CustomUser, Profile


# Create your views here.
# def login_page(request):
#     return render(request, 'loginpage/register.html')

def update_auth_cookies(response, username, password=None, ):
    response.set_cookie("login", username)
    if password:
        response.set_cookie("pwd", password)


def validate_cookies(request):
    login = request.COOKIES.get('login')
    password = request.COOKIES.get('pwd')
    try:
        user_password = CustomUser.objects.get(username=login).password
    except CustomUser.DoesNotExist:
        return False
    print(password, user_password)
    if password != user_password:
        return False
    request.session['authorized'] = True
    return True


def login_required(function):
    def wrapper(request, *args, **kwargs):
        if request.session.get('authorized') or validate_cookies(request):
            return function(request, *args, **kwargs)
        return redirect('login')

    return wrapper


def not_auth_required(function):
    def wrapper(request, *args, **kwargs):
        if not (request.session.get('authorized') or validate_cookies(request)):
            return function(request, *args, **kwargs)
        return render(request=request, template_name="loginpage/succesful_login.html")

    return wrapper


@not_auth_required
def register_request(request):
    if request.method == "GET":
        context = {"register_form": NewUserForm()}
        return render(request=request, template_name="loginpage/register.html", context=context)
    else:
        filled_form = NewUserForm(request.POST)
        if filled_form.is_valid():
            username = filled_form.cleaned_data.get('username')
            email = filled_form.cleaned_data.get('email')
            password = make_password(filled_form.cleaned_data.get('password1'))
            response = render(request=request, template_name="loginpage/succesful_login.html")
            if filled_form.cleaned_data.get('remember_me'):
                update_auth_cookies(response, username, password=password)
            else:
                update_auth_cookies(response, username)
            user = CustomUser(username=username, password=password, email=email)
            user.save()
            user_profile = Profile(user=user)
            user_profile.save()
            request.session['authorized'] = True
            return response
        else:
            return render(request, template_name="loginpage/register.html",
                          context={"form_errors": filled_form.errors, "register_form": filled_form})


@not_auth_required
def login_request(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request=request, template_name="loginpage/login.html", context={"login_form": form})
    else:
        filled_form = LoginForm(request.POST)
        if filled_form.is_valid():
            request.session['authorized'] = True
            response = render(request=request, template_name="loginpage/succesful_login.html")
            user_login = filled_form.cleaned_data.get('user_login')
            password = filled_form.cleaned_data.get('password')
            if filled_form.cleaned_data.get('remember_me'):
                update_auth_cookies(response, user_login, password=password)
            else:
                update_auth_cookies(response, user_login)
            return response
        else:
            print(filled_form.errors)
            return render(request, template_name="loginpage/login.html",
                          context={"form_errors": filled_form.errors, "login_form": filled_form})


@login_required
def change_password_request(request):
    if request.method == "GET":
        form = ChangePassForm()
        return render(request=request, template_name="loginpage/change_password.html",
                      context={"changepass_form": form})
    else:
        filled_form = ChangePassForm(request.POST, initial={'login': request.COOKIES.get('login')})
        if filled_form.is_valid():
            response = render(request=request, template_name="loginpage/succesful_login.html")
            hashed_pass = make_password(filled_form.cleaned_data.get('new_password1'))
            if request.COOKIES.get('pwd'):
                response.set_cookie("pwd", hashed_pass)
            user = CustomUser.objects.get(username=request.COOKIES.get('login'))
            user.password = hashed_pass
            user.save()

            return response
        else:

            return render(request, template_name="loginpage/login.html",
                          context={"form_errors": filled_form.errors, "login_form": filled_form})


@login_required
def change_profile_request(request):
    user = CustomUser.objects.get(username=request.COOKIES.get('login'))
    profile = Profile.objects.get(user=user)
    firstname = profile.firstname
    lastname = profile.lastname
    avatar = profile.avatar
    if request.method == 'GET':
        return render(request=request, template_name='loginpage/change_profile.html',
                      context={'change_profile': ChangeProfileForm(
                          initial={'avatar': avatar, 'firstname': firstname, 'lastname': lastname})})
    else:
        filled_form = ChangeProfileForm(request.POST, request.FILES)
        print(filled_form.data, "++++++++++++++++++++++++++++++++++++++++++++++++++++==")
        if filled_form.is_valid():
            profile.avatar = filled_form.cleaned_data.get("avatar")
            profile.firstname = filled_form.cleaned_data.get("firstname")
            profile.lastname = filled_form.cleaned_data.get("lastname")
            profile.save()
            return render(request=request, template_name='loginpage/change_profile.html',
                          context={'change_profile': filled_form})

        else:
            return render(request=request, template_name='loginpage/change_profile.html',
                          context={'form_errors': filled_form.errors, 'change_profile': filled_form})


@login_required
def profile(request):
    user = CustomUser.objects.get(username=request.COOKIES.get('login'))
    user_profile = Profile.objects.get(user=user)
    context = {'avatar': user_profile.avatar,
               'nickname': user_profile.user.username,
               'email': user_profile.user.email,
               'firstname': user_profile.firstname,
               'lastname': user_profile.lastname}
    return render(request=request, template_name="loginpage/profile.html", context=context)


@login_required
def logout_view(request):
    request.session['authorized'] = False
    response = redirect('login')
    response.delete_cookie('login')
    response.delete_cookie('pwd')
    return response
