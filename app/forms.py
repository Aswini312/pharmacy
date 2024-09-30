from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Product



class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ':'True','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(label=' Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    


    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description','product_image','expiry_date','mg','net_quantity','batch_no','brand','item_form','age_range','item_dimension','availability_status']
              
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'title', 'price', 'description','product_image','expiry_date','mg','net_quantity','batch_no','brand','item_form','age_range','item_dimension','availability_status']
              
       