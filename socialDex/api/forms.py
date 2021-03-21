from django import forms
from django.core.cache import cache

non_allowed_words = 'hack'


class PostForm(forms.Form):
	title = forms.CharField(required=True, max_length=100)
	composition = forms.CharField(label='Content',
								  required=True,
								  widget=forms.Textarea(attrs={'class': 'materialize-textarea',
															   'id': 'textarea1',
															   })
								  )
	user = forms.CharField(widget=forms.HiddenInput)

	def clean(self):
		cleaned_data = super().clean()
		title = self.cleaned_data.get('title')
		composition = self.cleaned_data.get('composition')
		user = self.cleaned_data.get('user')
		if non_allowed_words in title:
			cache.incr(f'{user}_not_allowed',1)
			raise forms.ValidationError('This content is not allowed.')
		elif non_allowed_words in composition:
			cache.incr(f'{user}_not_allowed',1)
			raise forms.ValidationError('This content is not allowed.')
		return cleaned_data