from django import forms
from django.contrib.auth.models import User
from .models import Profile, Order, BRAND_CHOICES, CATEGORY_CHOICES


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []  # Убираем avatar


class OrderForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.RadioSelect,
        label="Категория"
    )
    brand = forms.ChoiceField(
        choices=[],  # Заполним динамически в __init__
        widget=forms.RadioSelect,
        label="Бренд"
    )

    class Meta:
        model = Order
        fields = ['title', 'description', 'category', 'brand', 'image']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        if 'category' in self.data:
            category = self.data.get('category')
        elif self.instance.pk:
            category = self.instance.category
        else:
            category = None

        self.fields['brand'].choices = BRAND_CHOICES.get(category, [("", "Выберите бренд")])
