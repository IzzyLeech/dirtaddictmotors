from django import forms
from .models import Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field,  Fieldset


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'postcode', 'town_or_city', 'county',
            'country',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.label_class = ''
        self.helper.layout = Div(
            Fieldset(
                'Personal Information',
                Field('full_name', placeholder='Full Name *'),
                Field('email', placeholder='Email Address *'),
                css_class='fieldset-class',
            ),
            Fieldset(
                'Address Information',
                Field('phone_number', placeholder='Phone Number *'),
                Field('street_address1', placeholder='Street Address 1 *'),
                Field('street_address2', placeholder='Street Address 2', ),
                Field('postcode', placeholder='Postal Code'),
                Field('town_or_city', placeholder='Town or City'),
                Field('county', placeholder='County, State or Locality *'),
                Field('country', placeholder='Country '),
                css_class='fieldset-class',
            ),
        )
