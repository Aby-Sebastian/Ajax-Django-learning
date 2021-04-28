from django.forms import ModelForm, TextInput, CharField

from .models import Customer


class CreateCustomLinkForm(ModelForm):
	short_url = CharField(empty_value=True,required=False, widget=TextInput(attrs={'class':"form-control url-inp", 'id':"short_url", 'name':"short_url", 'placeholder':"Custom short url"}))

	class Meta:
		model = Customer
		fields = ['url','short_url']
		widgets = {
			'url' : TextInput(attrs={"class":"form-control", "id":"url", 'placeholder':"Enter url"}),
			
		}