
from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import CustomUser


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','username', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя на сайте',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
            'email': '@gmail.com',
        }

        for field, text in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs.update({'placeholder': text})

class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','username']
