from django import forms


class DocumentForm(forms.Form):
    file = forms.FileField(label='select file to upload')