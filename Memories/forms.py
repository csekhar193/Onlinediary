from django.contrib.auth.models import User
from django import forms
from django.db.models import TextField
from django.contrib.auth.forms import UserCreationForm
from Memories.models import Todays_memory

class MyRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	password1 =forms.CharField(widget=forms.PasswordInput)
	password2 =forms.CharField(widget=forms.PasswordInput)
	First_name = forms.CharField(required=True)
	Last_name = forms.CharField(required=True)
		
	class Meta:
		model = User
		fields = ('First_name','Last_name','username', 'email', 'password1','password2')

	def save(self, commit=True):
		user =super(MyRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.First_name = self.cleaned_data['First_name']
		user.Last_name = self.cleaned_data['Last_name']

		if commit:
			user.save()
		return user

class MemoryForm(forms.ModelForm):
	
	title = forms.CharField(required=True)
	text = forms.CharField(widget=forms.Textarea(attrs={
			'id': 'notes'}))
	class Meta:
		model = Todays_memory
		fields = ('title','text')










