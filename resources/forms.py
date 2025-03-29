from django import forms

class PostForm(forms.Form):
    title = forms.CharField(required=True, max_length=100)
    file = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'accept': '.md'}))

