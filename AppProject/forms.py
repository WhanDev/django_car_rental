from django import forms
from .models import *


class CarBrandForm(forms.ModelForm):
    class Meta:
        model = CarBarnd
        fields = ('name',)  # Note the comma after 'name' to make it a tuple
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
        }
        labels = {
            'name': 'ยี่ห้อรถ',
        }

    def deleteForm(self):
        self.fields['name'].widget.attrs['readonly'] = True


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('car_id', 'brand', 'model', 'type', 'price', 'rental_rate', 'picture')
        widgets = {
            'car_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 5}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'Min': 0}),
            'rental_rate': forms.NumberInput(attrs={'class': 'form-control', 'Min': 0}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'car_id': 'รหัสรถ',
            'brand': 'ยี่ห้อ',
            'model': 'รุ่นรถ',
            'type': 'ประเภทรถ',
            'price': 'ค่าเช่า',
            'rental_rate': 'อัตราค่าเช่า',
            'picture': 'รูปภาพ',
        }

    def updateForm(self):
        self.fields['car_id'].widget.attrs['readonly'] = True
        self.fields['car_id'].label = 'รหัสรถ [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['car_id'].widget.attrs['readonly'] = True
        self.fields['brand'].widget.attrs['readonly'] = True
        self.fields['model'].widget.attrs['readonly'] = True
        self.fields['type'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['rental_rate'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True