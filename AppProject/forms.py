from django import forms
from .models import *

class CarBarndForm(forms.ModelForm):
    class Meta:
        model = CarBarnd
        fields = ('name')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','maxlength':100}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'name': 'ยี่ห้อรถ'
        }
    def deleteForm(self):
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['desc'].widget.attrs['readonly'] = True