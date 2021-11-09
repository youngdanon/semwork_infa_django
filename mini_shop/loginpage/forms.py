from django import forms
from django.contrib.auth.hashers import check_password

from .models import CustomUser, Profile

User = CustomUser


# Create your forms here.

class NewUserForm(forms.Form):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')

    username = forms.CharField(required=True,
                               label='Имя пользователя')

    password1 = forms.CharField(required=True,
                                widget=forms.PasswordInput,
                                label='Пароль',
                                help_text='Пароль должен быть длиннее 8 символов')

    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput,
                                label='Повторите пароль')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        print(password1, password2)
        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Такой email уже используется')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Имя пользователя занято')

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        default_passwords = ['qwerty', '12345']
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать более 8 символов')
        return password
        # if password in default_passwords:
        #     raise forms.ValidationError('Слишком простой пароль')


class LoginForm(forms.Form):
    user_login = forms.CharField(required=True, label='Имя пользователя или почта')
    password = forms.CharField(required=True, widget=forms.PasswordInput, label='Ваш пароль')
    remember_me = forms.BooleanField(required=False, label='Запомнить меня')

    def clean_user_login(self):
        user_login = self.cleaned_data.get("user_login")
        try:
            User.objects.get(username=user_login)
        except User.DoesNotExist:
            try:
                User.objects.get(email=user_login)
            except User.DoesNotExist:
                raise forms.ValidationError('Неверный Email или имя пользователя')
        return user_login

    def clean_password(self):
        user_login = self.cleaned_data.get("user_login")
        password = self.cleaned_data.get('password')
        try:
            user_password = User.objects.get(username=user_login).password
        except User.DoesNotExist:
            user_password = User.objects.get(email=user_login).password
        if not check_password(password, user_password):
            raise forms.ValidationError('Неверный пароль')
        return user_password
