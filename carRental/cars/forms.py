from django import forms

from .models import Car, Discount


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'year', 'car_type', 'transmission',
            'fuel', 'seats', 'license_plate', 'daily_rate',
            'image', 'is_available',
        ]
        widgets = {
            'image': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['code', 'percentage', 'valid_from', 'valid_until']
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        data = super().clean()
        if data.get('valid_from') and data.get('valid_until'):
            if data['valid_until'] < data['valid_from']:
                raise forms.ValidationError('valid_until must be after valid_from.')
        pct = data.get('percentage')
        if pct is not None and (pct < 1 or pct > 100):
            self.add_error('percentage', 'Percentage must be between 1 and 100.')
        return data
