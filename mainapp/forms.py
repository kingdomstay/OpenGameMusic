from django import forms
from django.contrib.auth.models import User

from mainapp.models import Track

GROUP_CHOICES = [
    ('Developers', 'Я разработчик'),
    ('Artists', 'Я музыкант'),
]


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.wav', '.mp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Поддерживаемые типы файлов: .mp3, .wav')


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    group = forms.CharField(label='Ваша роль', widget=forms.RadioSelect(choices=GROUP_CHOICES))

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class AristUploadingTrackForm(forms.ModelForm):
    title = forms.CharField(label='Название трека', max_length=30)
    file = forms.FileField(label='Перетащите трек в поле ниже', validators=[validate_file_extension])

    class Meta:
        model = Track
        fields = ('title',)
