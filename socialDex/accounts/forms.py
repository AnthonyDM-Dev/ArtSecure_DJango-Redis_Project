from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.cache import cache

User = get_user_model()
non_allowed_words = 'hack'


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
																 'id': 'user-password'}))
	ip_address = forms.CharField(widget=forms.HiddenInput)


	def clean(self):
		cleaned_data = super().clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		ip_address = self.cleaned_data.get('ip_address')
		qs = User.objects.filter(username__iexact=username)
		if not qs.exists():
			cache.incr(f'{ip_address}_attempt', 1)
			raise forms.ValidationError('Invalid user.')
		else:
			user = qs.get(username=username)
			if check_password(password, user.password) == False:
				cache.incr(f'{ip_address}_attempt', 1)
				raise forms.ValidationError('Invalid password.')
		return cleaned_data


class PasswordForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'class': 'form-control',
																					   'id': 'user-password',}))
	new_password = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control',
																						   'id': 'user-password',}))
	confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control',
																								   'id': 'user-password',}))

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username__iexact=username)
		if not qs.exists():
			raise forms.ValidationError('Invalid user.')
		return username

	def clean(self):
		cleaned_data = super().clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		qs = User.objects.filter(username__iexact=username)
		if qs.exists():
			user = qs.get(username=username)
			if check_password(password, user.password) == False:
				raise forms.ValidationError('Invalid password.')
			else:
				if new_password != confirm_password:
					raise forms.ValidationError('New password and password confirmation do not match.')
		return cleaned_data

class RegisterForm(forms.Form):
	username = forms.CharField()
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control',
																				   'id': 'user-password',}))
	ip_address = forms.CharField(widget=forms.HiddenInput)

	def clean(self):
		cleaned_data = super().clean()
		username = self.cleaned_data.get('username')
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		ip_address = self.cleaned_data.get('ip_address')
		if non_allowed_words in username:
			cache.incr(f'{ip_address}_hacking', 1)
			raise forms.ValidationError('This username is not valid, please pick another one.')
		if non_allowed_words in first_name:
			cache.incr(f'{ip_address}_hacking', 1)
			raise forms.ValidationError('First name not valid, please pick another one.')
		if non_allowed_words in last_name:
			cache.incr(f'{ip_address}_hacking', 1)
			raise forms.ValidationError('Last name not valid, please pick another one.')
		if non_allowed_words in email:
			cache.incr(f'{ip_address}_hacking', 1)
			raise forms.ValidationError('This email is not valid, please pick another one.')
		if non_allowed_words in password:
			cache.incr(f'{ip_address}_hacking', 1)
			raise forms.ValidationError('Password not valid, please pick another one.')
		qs_users = User.objects.filter(username__iexact=username)
		if qs_users.exists():
			raise forms.ValidationError('This username is not valid, please pick another one.')
		qs_emails = User.objects.filter(email__iexact=email)
		if qs_emails.exists():
			raise forms.ValidationError('This email is already in use, please pick another one.')
		return cleaned_data