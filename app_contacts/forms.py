from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm, CharField, TextInput, DateInput, Textarea, ModelChoiceField, Select, SelectMultiple, \
    MultipleChoiceField, BooleanField, CheckboxInput, DateField

from app_contacts.models import Contact, Address


class ContactForm(ModelForm):
    name = CharField(min_length=3, max_length=20, required=True,
                     widget=TextInput(attrs={'placeholder': 'Name', "class": "form-control"}))
    surname = CharField(min_length=3, max_length=20, required=False,
                        widget=TextInput(attrs={'placeholder': 'Surname', "class": "form-control"}))
    email = CharField(required=False, validators=[
        RegexValidator(regex=r'^[a-zA-Z0-9_.+-]{1}[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]{2,}',
                       message='Enter a valid email address.')],
                      widget=TextInput(attrs={'placeholder': 'Email', "class": "form-control"}))
    mobile_phone = CharField(required=False, validators=[RegexValidator(
        regex=r'\+?\d{1,3}\(?\d{2,4}\)?\d{3}(?:-?\d{3,4})(\d{3})?',
        message='Phone number must be entered in the format: +CountryCode(operator code)phone number example: +380(50)1234567. Up to 15 digits allowed.'
    )],
                             widget=TextInput(attrs={'placeholder': 'Mobile phone', "class": "form-control"}))
    work_phone = CharField(required=False, validators=[RegexValidator(
        regex=r'\+?\d{1,3}\(?\d{2,4}\)?\d{3}(?:-?\d{3,4})(\d{3})?',
        message='Phone number must be entered in the format: +CountryCode(operator code)phone number example: +380(50)1234567. Up to 15 digits allowed.'
    )],
                           widget=TextInput(attrs={'placeholder': 'Work phone', "class": "form-control"}))
    home_phone = CharField(required=False, validators=[RegexValidator(
        regex=r'\+?\d{1,3}\(?\d{2,4}\)?\d{3}(?:-?\d{3,4})(\d{3})?',
        message='Phone number must be entered in the format: +CountryCode(operator code)phone number example: +380(50)1234567. Up to 15 digits allowed.'
    )],
                           widget=TextInput(attrs={'placeholder': 'Home phone', "class": "form-control"}))
    birthdate = DateField(required=False, input_formats=['%d/%m/%Y'], widget=DateInput(format='%d/%m/%Y'))
    facebook = CharField(required=False, validators=[RegexValidator(
        regex=r'^https?://(www\.)?facebook\.com/.+',
        message='Enter a valid Facebook URL.',
    )], widget=TextInput(attrs={'placeholder': 'https://facebook.com', "class": "form-control"}))
    instagram = CharField(required=False, validators=[RegexValidator(
        regex=r'^https?://(www\.)?instagram\.com/.+',
        message='Enter a valid Instagram URL.',
    )], widget=TextInput(attrs={"placeholder": 'https://instagram.com', "class": "form-control"}))
    tiktok = CharField(required=False, validators=[RegexValidator(
        regex=r'^https?://(www\.)?tiktok\.com/.+',
        message='Enter a valid Tiktok URL.',
    )], widget=TextInput(attrs={"placeholder": 'https://tiktok.com', "class": "form-control"}))
    is_favorite = BooleanField(required=False, label='Is favorite',
                               widget=CheckboxInput(attrs={'placeholder': 'is_favorite', "class": "form-check-input"}))

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'email', 'mobile_phone', 'work_phone', 'home_phone', 'birthdate', 'is_favorite',
                  'facebook', 'instagram', 'tiktok', ]
        widgets = {
            'birthdate': DateInput(attrs={'type': 'date'}),
        }


class AddressForm(ModelForm):
    country = CharField(required=False, widget=TextInput(attrs={'placeholder': 'Country', "class": "form-control"}))
    city = CharField(required=False, widget=TextInput(attrs={'placeholder': 'City', "class": "form-control"}))
    address = CharField(required=False, widget=TextInput(attrs={'placeholder': 'Address', "class": "form-control"}))

    class Meta:
        model = Address
        fields = ['country', 'city', 'address']
        # widgets = {
        #     'name': TextInput(attrs={'placeholder': 'Name'}),
        #     'surname': TextInput(attrs={'placeholder': 'Surname'}),
        #     'email': TextInput(attrs={'placeholder': 'Email'}),
        #     'mobile_phone': TextInput(attrs={'placeholder': 'Mobile phone'}),
        #     'work_phone': TextInput(attrs={'placeholder': 'Work phone'}),
        #     'home_phone': TextInput(attrs={'placeholder': 'Home phone'}),
        #     'birthdate': DateInput(attrs={'type': 'date'}),
        #     'is_favorite': Select(attrs={'placeholder': 'Is favorite'}),
        # }

# class ContactUpdateForm(ModelForm):
#     name = CharField(min_length=3, max_length=20, required=False,
#                      widget=TextInput(attrs={"class": "form-control"}))
#     surname = CharField(min_length=3, max_length=20, required=False,
#                         widget=TextInput(attrs={"class": "form-control"}))
#     email = CharField(required=False, widget=TextInput(attrs={"class": "form-control"}))
#     mobile_phone = CharField(required=False,
#                              widget=TextInput(attrs={"class": "form-control"}))
#     work_phone = CharField(required=False,
#                            widget=TextInput(attrs={"class": "form-control"}))
#     home_phone = CharField(required=False,
#                            widget=TextInput(attrs={"class": "form-control"}))
#     birthdate = DateInput(attrs={'type': 'date', "class": "form-control"})
#     facebook = CharField(required=False, validators=[RegexValidator(
#         regex=r'^https?://(www\.)?facebook\.com/.+',
#         message='Enter a valid Facebook URL.',
#     )], widget=TextInput(attrs={"class": "form-control"}))
#     instagram = CharField(required=False, widget=TextInput(attrs={"class": "form-control"}))
#     tiktok = CharField(required=False, widget=TextInput(attrs={"class": "form-control"}))
#     is_favorite = BooleanField(label='Is favorite', required=False,
#                                widget=CheckboxInput(attrs={"class": "form-check-input"}))
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if email:
#             qs = Contact.objects.exclude(pk=self.instance.pk)
#             if qs.filter(email=email).exists():
#                 raise forms.ValidationError("Email already exists")
#         return email
#
#     class Meta:
#         model = Contact
#         fields = ['name', 'surname', 'email', 'mobile_phone', 'work_phone', 'home_phone', 'birthdate', 'is_favorite',
#                   'facebook', 'instagram', 'tiktok', ]
