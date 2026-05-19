from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None

        self.fields['username'].error_messages.update({
            'required': 'Пожалуйста, введите имя пользователя.',
            'unique': 'Пользователь с таким именем уже существует.',
            'invalid': 'Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_.',
        })
        self.fields['password1'].error_messages.update({
            'required': 'Пожалуйста, введите пароль.',
        })
        self.fields['password2'].error_messages.update({
            'required': 'Пожалуйста, подтвердите пароль.',
        })

    def clean_password2(self):
        """Переопределяем проверку пароля, чтобы выдать своё сообщение"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2


class CustomAuthenticationForm(AuthenticationForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None

        self.fields['username'].error_messages.update({
            'required': 'Введите имя пользователя.',
        })
        self.fields['password'].error_messages.update({
            'required': 'Введите пароль.',
        })

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Учётная запись неактивна. Обратитесь к администратору.",
                code='inactive',
            )
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    last_name = forms.CharField(max_length=30, required=False, label='Фамилия')
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta:
        model = Profile
        fields = ['role', 'year', 'group_name', 'avatar']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_year'}),
            'group_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_group_name'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        year = cleaned_data.get('year')
        group_name = cleaned_data.get('group_name')

        if role in ['student', 'graduate']:
            if not year:
                self.add_error('year', 'Укажите год.')
            if not group_name:
                self.add_error('group_name', 'Укажите группу.')
        else:
            cleaned_data['year'] = None
            cleaned_data['group_name'] = ''
        return cleaned_data

    def save(self, commit=True, user=None):
        profile = super().save(commit=False)
        profile.year = self.cleaned_data.get('year')
        profile.group_name = self.cleaned_data.get('group_name', '')
        if commit:
            profile.save()
            if user:
                user.first_name = self.cleaned_data.get('first_name', '')
                user.last_name = self.cleaned_data.get('last_name', '')
                user.email = self.cleaned_data.get('email', '')
                user.save()
        return profile


class ExcursionBookingForm(forms.ModelForm):
    class Meta:
        model = ExcursionBooking
        fields = "__all__"
        labels = {
            'name': 'Имя',
            'email': 'Email',
            'phone': 'Телефон',
            'date': 'Дата',
            'time': 'Время',
            'people_count': 'Количество человек'
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'time': forms.Select(attrs={'class': 'form-input'}, choices=[
                ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'),
                ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'),
                ('16:00', '16:00'), ('17:00', '17:00'),
            ]),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иван Петров'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@mail.ru'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (999) 123-45-67'}),
            'people_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 20, 'value': 5}),
            'comments': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Особые пожелания...'}),}
