from django import forms
from .models import Bikes
from .widgets import CustomClearableFileInput


class BikeForm(forms.ModelForm):

    class Meta:
        model = Bikes
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)
