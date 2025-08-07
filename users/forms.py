
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','username', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Имя'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Фамилия'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Имя пользователя на сайте'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите пароль'})
        self.fields['email'].widget.attrs.update({'placeholder': '@gmail.com'})
