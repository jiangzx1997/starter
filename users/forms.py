import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Group

class RegistrationForm(forms.Form):
    username = forms.CharField(label = 'Username:', max_length = 30)
    email = forms.EmailField(label = 'Email:')
    name = forms.CharField(label = 'Name:', max_length = 20)
    number = forms.CharField(label = 'Number:', max_length = 30)
    password1 = forms.CharField(label = 'Password:', widget = forms.PasswordInput())
    password2 = forms.CharField(label = 'Password(Again):', widget = forms.PasswordInput())
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
        if password1 == password2:
            return password2
        raise forms.ValidationError('Passwords do not match.')
        
    def clean_username(self):
        Username = self.cleaned_data['username']
        if not re.search(r'^\w+$', Username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username = Username)
        except ObjectDoesNotExist:
            return Username
        raise forms.ValidationError('Username is already taken.')
    
    def clean_number(self):
        Number = self.cleaned_data['number']
        if len(Number) != 8:
            raise forms.ValidationError('The length of the User number must be 8')
        for c in Number:
            if c < '0' or c > '9':
                raise forms.ValidationError('User number can only contain 0 .. 9')
        for user in User.objects.all():
            if user.myuser.number == Number:
                raise forms.ValidationError('Usernumber is already taken.')
        return Number

class GroupForm(forms.ModelForm):
#    name = forms.CharField(label = 'Group Name:', max_length = 30)
    class Meta:
        model = Group
        fields = ['name']
        labels = {'name':'Group Name:'}

class MemberIDForm(forms.Form):
    userID = forms.CharField(label = 'Add member:', max_length = 8)
    userID.widget.attrs['placeholder'] = 'User number'
    userID.widget.attrs['size'] = 10
    key = forms.CharField(widget=forms.HiddenInput(attrs={'key':''}))
    
    def clean_userID(self):
        Number = self.cleaned_data['userID']
        if len(Number) != 8:
            raise forms.ValidationError('The length of the User number must be 8')
        for c in Number:
            if c < '0' or c > '9':
                raise forms.ValidationError('User number can only contain 0 .. 9')
        flag = False
        for user in User.objects.all():
            if user.myuser.number == Number:
                flag = True
                break
        if not flag:
            raise forms.ValidationError('No such member')
        return Number
