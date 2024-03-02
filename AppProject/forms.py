from django import forms
from .models import *

class CarBarndForm(forms.ModelForm):
    class Meta:
        model = CarBarnd
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','maxlength':100}),

        }
        labels = {
            'name': 'ยี่ห้อรถ'
        }
    def deleteForm(self):
        self.fields['name'].widget.attrs['readonly'] = True


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
        