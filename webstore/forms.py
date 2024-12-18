from django import forms
from .models import Menu,ShippingDetails


class AddMenuForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
    description = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={"placeholder":"Description", "class":"form-control"}), label="")
    price=forms.FloatField(widget=forms.NumberInput(attrs={'step': 0.01,'placeholder': 'Enter price','min': '0', "class":"form-control"}),label='Price')

    class Meta:
        model = Menu
        exclude = ("user",)



class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        fields = ['name', 'delivery_date', 'delivery_time', 'house_no', 'street1', 'street2', 'town', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'delivery_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'delivery_time': forms.TextInput(attrs={'class': 'form-control'}),
            'house_no':forms.TextInput(attrs={'class': 'form-control'}),
            'street1':forms.TextInput(attrs={'class': 'form-control'}),
            'street2':forms.TextInput(attrs={'class': 'form-control'}), 
            'town':forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),

        }        
