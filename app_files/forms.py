from django.forms import ModelForm, FileField, FileInput, CharField, TextInput
from .models import UserFile


class UploadFileForm(ModelForm):
    filepath = FileField(widget=FileInput(attrs={'class': 'form-control'}))
    file_description = CharField(max_length=255, required=False, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserFile
        fields = ['filepath', 'file_description']
        exclude = ['user']
