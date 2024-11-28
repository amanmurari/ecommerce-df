from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User

class LoginFrom(forms.ModelForm):
    email= forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={"autofocus": True,"class":"form-control","placeholder":"Enter Your email address"}))
    password= forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Your password"}))
    
    class Meta:
        model = User
        
        fields = ['email', 'password']


class SignUpFrom(forms.ModelForm):
    username= UsernameField(max_length=200,widget=forms.TextInput(attrs={"autofocus": True,"class":"form-control","placeholder":"Enter Your username"}))
    email= forms.EmailField(max_length=200,widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Your email address"}))
    password1= forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Your password"}))
    password2= forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter the same password"}))

    class Meta:
        model = User
        
        fields = ["first_name","last_name",'username','email', 'password1','password2']

