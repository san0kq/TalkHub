from django import forms


class CreateTweetForm(forms.Form):
    text = forms.CharField(label="Text", max_length=400, widget=forms.Textarea)
