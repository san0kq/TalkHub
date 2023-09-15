from django import forms


class SearchTagForm(forms.Form):
    name = forms.CharField(label="Tag", max_length=30, strip=True, required=False)
