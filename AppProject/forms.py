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
        fields = ('car_id', 'brand', 'model', 'gear', 'car_cc','picture')
        widgets = {
            'car_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 5}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
            'gear': forms.Select(attrs={'class': 'form-control'}),
            'car_cc': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'car_id': 'รหัสรถ',
            'brand': 'ยี่ห้อ',
            'model': 'รุ่นรถ',
            'gear': 'ประเภทเกียร์',
            'car_cc': 'ปริมาณ CC',
            'picture': 'รูปภาพ',
        }

    def updateForm(self):
        self.fields['car_id'].widget.attrs['readonly'] = True
        self.fields['car_id'].label = 'รหัสรถ [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['car_id'].widget.attrs['readonly'] = True
        self.fields['brand'].widget.attrs['readonly'] = True
        self.fields['model'].widget.attrs['readonly'] = True
        self.fields['gear'].widget.attrs['readonly'] = True
        self.fields['car_cc'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True

        self.fields['car_id'].widget.attrs['disabled'] = True
        self.fields['brand'].widget.attrs['disabled'] = True
        self.fields['model'].widget.attrs['disabled'] = True
        self.fields['gear'].widget.attrs['disabled'] = True
        self.fields['car_cc'].widget.attrs['disabled'] = True
        self.fields['picture'].widget.attrs['disabled'] = True

class EmployForm(forms.ModelForm):
    ROLES = [
        ('employee', 'พนักงาน'),
        ('admin', 'แอดมิน'),
    ]
    class Meta:
        model = Employ
        fields = ('em_id', 'email', 'name', 'tell', 'address', 'role')
        widgets = {
            'em_id': forms.TextInput(attrs={'class': 'form-control', 'size': 15, 'maxlength': 13}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'size': 60, 'maxlength': 50}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'size': 60, 'maxlength': 50}),
            'tell': forms.TextInput(attrs={'class': 'form-control', 'size': 10, 'maxlength': 10}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'size': 50, 'maxlength': 50}),
            'role': forms.Select(choices=ROLES, attrs={'class': 'form-control'}),
        }
        labels = {
            'em_id': 'รหัสพนักงาน',
            'email': 'อีเมลล์',
            'name': 'ชื่อพนักงาน',
            'tell': 'เบอร์โทร',
            'address': 'ที่อยู่',
            'role': 'สิทธิผู้ใช้งาน',
        }

