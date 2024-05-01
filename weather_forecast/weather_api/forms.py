from django import forms


class WeatherForm(forms.Form):
    latitude = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'})
    )
    longitude = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'})
    )
    forecast_type = forms.ChoiceField(
        choices=[
            ('', '--- Select Forecast Type ---'),
            ('current', 'Current Weather'),
            ('3-hourly', '3 Hour Forecast for 5 days'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
