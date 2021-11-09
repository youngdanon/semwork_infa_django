from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm
from .models import CustomUser, Profile


# Create your views here.
# def login_page(request):
#     return render(request, 'loginpage/register.html')

def validate_cookies(request):
    login = request.COOKIES.get('login')
    password = request.COOKIES.get('pwd')
    try:
        user_password = CustomUser.objects.get(username=login).password
    except CustomUser.DoesNotExist:
        try:
            user_password = CustomUser.objects.get(email=login).password
        except CustomUser.DoesNotExist:
            return False
    print(password, user_password)
    if password != user_password:
        return False
    request.session['authorized'] = True
    return True


def login_required(function):
    def wrapper(request, *args, **kwargs):
        if request.session.get('authorized', None) or validate_cookies(request):
            return function(request, *args, **kwargs)
        return redirect('login')

    return wrapper


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
            profile = Profile(user=user)
            profile.save()
            request.session['authorized'] = True
            return render(request=request, template_name="loginpage/succesful_login.html")
        else:
            return render(request, template_name="loginpage/register.html",
                          context={"form_errors": filled_form.errors, "register_form": filled_form})


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
                response.set_cookie("login", filled_form.cleaned_data.get('user_login'))
                response.set_cookie("pwd", filled_form.cleaned_data.get('password'))
            return response
        else:
            return render(request, template_name="loginpage/login.html",
                          context={"form_errors": filled_form.errors, "login_form": filled_form})


@login_required
def profile(request):
    print(request.GET)
    print(request.profile.username)
    context = {'nickname': request.profile.username,
               'email': request.profile.email,
               'gender': 'Мужчина' if request.profile.gender == 'm' else 'Женщина',
               'firstname': request.profile.firstname,
               'lastname': request.profile.lastname}
    return render(request=request, template_name="loginpage/profile.html", context=context)


@login_required
def logout_view(request):
    request.session['authorized'] = False
    response = redirect('login')
    response.delete_cookie('login')
    response.delete_cookie('pwd')
    return response
