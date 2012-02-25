# -*- encoding: utf-8 -*-
'''
Created on 2012. 2. 13.

@author: kobe
'''
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import re
from django.utils.translation import gettext_lazy

# 사용자 등록 폼
class RegistrationForm(forms.Form):
    '''
    classdocs
    '''
    username = forms.CharField(label=gettext_lazy('User name'), max_length=30)
    email = forms.EmailField(label=gettext_lazy('e-mail'))
    password1 = forms.CharField(label=gettext_lazy('Password'), widget=forms.PasswordInput())
    password2 = forms.CharField(label=gettext_lazy('Confirm Password'), widget=forms.PasswordInput())
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Password does not match.')
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
#            raise forms.ValidationError('사용자 이름은 알파벳, 숫자, 밑줄(_)만 가능합니다.')
            raise forms.ValidationError('The user name letters of the alphabet, numbers, underscore are available.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
#        raise forms.ValidationError('이미 사용 중인 사용자 이름입니다.')
        raise forms.ValidationError('The user name is already in user.')

# 북마크 저장 폼 
class BookmarkSaveForm(forms.Form):
    url = forms.URLField(label=gettext_lazy('Address'), widget=forms.TextInput(attrs={'size': 64}))
    title = forms.CharField(label=gettext_lazy('Title'), widget=forms.TextInput(attrs={'size': 64}))
    tags = forms.CharField(label=gettext_lazy('Tag'), widget=forms.TextInput(attrs={'size': 64}))
    share = forms.BooleanField(label=gettext_lazy('On the first page is shared.'), required=False)
    
# 검색 폼
class SearchForm(forms.Form):
    query = forms.CharField(label=gettext_lazy('Please enter a search term.'), widget=forms.TextInput(attrs={'size': 32}))
    
    