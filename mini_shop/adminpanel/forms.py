from django import forms


class EditUserRole(forms.Form):
    is_admin = forms.BooleanField(label='Права админа', required=False)


class ProductForm(forms.Form):
    name = forms.CharField(label='Название товара', required=True)
    description = forms.CharField(label='Описание товара', required=True)
    price = forms.IntegerField(label='Цена в рублях')
    type = forms.CharField(label='Тип товара')
    weight = forms.IntegerField(label='Вес товара')

