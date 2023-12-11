from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'type', 'maker', 'price', 'digital', 'image', 'stock_no']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }