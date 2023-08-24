from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Password", max_length=128, widget=forms.PasswordInput)
