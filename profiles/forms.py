from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form that will store the user default inforamtion
    """

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = UserProfile
        fields = [
                    'first_name', 'last_name', 'default_phone_number',
                    'default_country', 'default_postcode',
                    'default_town_or_city', 'default_street_address1',
                    'default_street_address2', 'default_county']
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        user = self.instance.user
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]}*'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False
