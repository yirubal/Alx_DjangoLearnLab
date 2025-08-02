from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(max_length=100)


class ExampleForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
