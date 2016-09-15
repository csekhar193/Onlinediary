from django.contrib.auth.models import User
from django import forms
from django.db.models import TextField
from django.contrib.auth.forms import UserCreationForm
from Memories.models import Todays_memory, Comment, Profile

class MyRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	password1 =forms.CharField(widget=forms.PasswordInput)
	password2 =forms.CharField(widget=forms.PasswordInput)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
		
	class Meta:
		model = User
		fields = ('first_name','last_name','username', 'email', 'password1','password2')

	def save(self, commit=True):
		user = super(MyRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']

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

class CommentForm(forms.ModelForm):
	author = forms.CharField(required=True)
	text = forms.CharField(widget=forms.Textarea(attrs={
		'id': 'comment'}))
	class Meta:
		model = Comment
		fields = ('author', 'text')


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
	photo = forms.FileField(required=True)
	bio = forms.CharField(widget=forms.Textarea)
	phone = forms.CharField(required=True)
	city = forms.CharField(required=True)
	country = forms.CharField(required=True)
	class Meta:
		model = Profile
		fields = ('photo', 'birth_date','bio', 'phone', 'city', 'country')
		widgets = {
			'birth_date': DateInput(),

		}










