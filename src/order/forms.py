from django import forms
from .models import Sale


# Register your forms here.
class OrderSaleForm(forms.ModelForm):

    class Meta:
        model = Sale

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['maximum'].widget.attrs.update({'class': 'form-control'})
        self.fields['minimum'].widget.attrs.update({'class': 'form-control'})
