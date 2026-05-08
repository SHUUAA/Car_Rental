from django import forms

from cars.models import Discount

from .models import Booking, Payment, Review


class BookingForm(forms.ModelForm):
    discount_code = forms.CharField(max_length=20, required=False,
                                    help_text='Optional discount code')

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        data = super().clean()
        sd, ed = data.get('start_date'), data.get('end_date')
        if sd and ed and ed < sd:
            raise forms.ValidationError('End date must be on or after start date.')
        code = (data.get('discount_code') or '').strip()
        if code:
            try:
                discount = Discount.objects.get(code=code)
            except Discount.DoesNotExist:
                self.add_error('discount_code', 'No such discount code.')
            else:
                if sd and (discount.valid_from > sd or discount.valid_until < sd):
                    self.add_error('discount_code', 'Code not valid for those dates.')
                else:
                    data['discount'] = discount
        return data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method']


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
