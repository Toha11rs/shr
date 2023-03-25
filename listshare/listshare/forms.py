from django import forms
from shares.models import Share


class BuyShareForm(forms.Form):
    ticker = forms.CharField(max_length=10)
    quantity = forms.IntegerField(min_value=1)

    def clean_ticker(self):
        ticker = self.cleaned_data['ticker'].upper()
        if not Share.objects.filter(ticker=ticker).exists():
            raise forms.ValidationError(f'The ticker {ticker} does not exist.')
        return ticker

    def clean_quantity(self):
        ticker = self.cleaned_data.get('ticker')
        quantity = self.cleaned_data['quantity']
        if ticker and quantity > Share.objects.get(ticker=ticker).available_shares:
            raise forms.ValidationError(
                'Not enough shares available for purchase.')
        return quantity


class AddFundsForm(forms.Form):
    amount = forms.FloatField()
