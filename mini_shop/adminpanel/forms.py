from django import forms


class EditUserRole(forms.Form):
    is_admin = forms.BooleanField(label='Права админа', required=False)
