from django import forms
from django.contrib.auth import get_user_model,models

User=get_user_model()

class GuestForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control" , "placeholder":"Your Email"}))


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control" , "placeholder":"Your Full Name"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control" , "placeholder":"Password"}))

class RegisterForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control" , "placeholder":"Your Full Name"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control" , "placeholder":"Password"}))
    password2=forms.CharField(label="Confirm Password" , widget=forms.PasswordInput(attrs={"class":"form-control" , "placeholder":"Confirm your Password"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control" , "placeholder":"Your Email"}))

    class Meta():
        model = models.User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username=self.cleaned_data.get('username')
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Usernsme is taken")
        return username


    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords dont match")
        return data
