from django import forms
from django.contrib.auth.hashers import check_password

from .models import CustomUser, Profile

User = CustomUser


# Create your forms here.

class NewUserForm(forms.Form):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    username = forms.CharField(required=True, label='Имя пользователя')
    password1 = forms.CharField(required=True, widget=forms.PasswordInput,
                                label='Пароль', help_text='Не менее 8-ми символов')
    password2 = forms.CharField(required=True, widget=forms.PasswordInput, label='Повторите пароль')
    remember_me = forms.BooleanField(required=False, label='Запомнить это устройство')

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
    remember_me = forms.BooleanField(required=False, label='Запомнить это устройство')

    def clean_user_login(self):
        user_login = self.cleaned_data.get("user_login")
        try:
            user = User.objects.get(username=user_login)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=user_login)
            except User.DoesNotExist:
                raise forms.ValidationError('Неверный Email или имя пользователя')
        return user.username

    def clean_password(self):
        user_login = self.cleaned_data.get("user_login")
        password = self.cleaned_data.get('password')
        try:
            user_password = User.objects.get(username=user_login).password
        except User.DoesNotExist:
            try:
                user_password = User.objects.get(email=user_login).password
            except User.DoesNotExist:
                raise forms.ValidationError('')
        if not check_password(password, user_password):
            raise forms.ValidationError('Неверный пароль')
        return user_password


class ChangeProfileForm(forms.Form):
    firstname = forms.CharField(label='Имя')
    lastname = forms.CharField(label='Фамилия')

class ChangePassForm(forms.Form):
    old_password = forms.CharField(required=True,
                                   widget=forms.PasswordInput,
                                   label='Старый пароль')

    new_password1 = forms.CharField(required=True,
                                    widget=forms.PasswordInput,
                                    label='Новый пароль')
    new_password2 = forms.CharField(required=True,
                                    widget=forms.PasswordInput,
                                    label='Повторите новый пароль')

    def clean_old_password(self):
        login = self.initial.get('login')
        old_hashed_password = CustomUser.objects.get(username=login).password
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, old_hashed_password):
            raise forms.ValidationError('Вы ввели неправильный пароль')

    def clean_new_password1(self):
        password = self.cleaned_data.get("new_password1")
        default_passwords = ['qwerty', '12345']
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать более 8 символов')
        return password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
