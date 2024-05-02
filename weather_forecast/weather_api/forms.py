from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class WeatherForm(forms.Form):
    latitude = forms.DecimalField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'})
    )
    longitude = forms.DecimalField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'})
    )
    forecast_type = forms.ChoiceField(
        choices=[
            ('', '--- Select Forecast Type ---'),
            ('current', 'Current Weather'),
            ('3-hourly', '3 Hour Forecast for 5 days'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
