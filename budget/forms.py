from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User

from unidecode import unidecode

from .models import Operation, Category, Family


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name']


class OperationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['value', 'description', 'category']:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})
        self.fields['value'].widget.attrs.update({'min': 0})
        self.fields['description'].widget.attrs.update({'list': 'desc-list'})

    class Meta:
        model = Operation
        fields = ['value', 'description', 'category']

    def clean_value(self):
        value = self.cleaned_data['value']
        if value < 0 or value == 0:
            raise ValidationError("Введено некорректное значение")
        return value


class CategoryForm(forms.ModelForm):
    user_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['name', 'type_pay']:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})

    class Meta:
        model = Category
        fields = ['name', 'type_pay', 'user_id']

    def clean(self):
        user_id = self.cleaned_data['user_id']
        name = self.cleaned_data['name']
        type_pay = self.cleaned_data['type_pay']

        if Category.objects.filter(user_id=user_id, name=name, type_pay=type_pay).exists():
            raise ValidationError({'name': 'Категория уже существует'})
        return self.cleaned_data
# class UserForm(forms.Form):
#     login = forms.CharField(max_length=32, required=True, widget=forms.TextInput(
#         attrs={'style': 'color: red;', 'class': 'form-control'}))
#     password = forms.CharField(min_length=1, required=True, widget=forms.PasswordInput(
#         attrs={'style': 'color: red;', 'class': 'form-control'}))
#     select = forms.MultipleChoiceField(choices=[('1', '1'), ('2', '2'), ('3', '3')], widget=forms.CheckboxSelectMultiple(
#         attrs={'class':'radio-choice'}))
#     slug = forms.CharField(label="СЛАГ", required=False, max_length=128)
#     slug.widget.attrs.update({'class': 'form-control'})
#     is_draft = forms.BooleanField(initial=False, widget=forms.CheckboxInput, required=False)
#
#     def clean_login(self):
#         login = self.cleaned_data['login']
#         if login == 'admin':
#             raise ValidationError('Логин занят')
#         return login
#
#     def clean_password(self):
#         #validate_password(self.cleaned_data['password'], password_validators=[MinimumLengthValidator()])
#         return self.cleaned_data['password']
#
#     def clean_slug(self):
#         return slugify(unidecode(self.cleaned_data['slug']))
