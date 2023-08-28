from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import RegisterModel , CityModel
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = RegisterModel
        fields = "__all__"
        
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if not dob:
            raise ValidationError('Date of birth is required.')

        mobile = self.cleaned_data.get('mobile')
        today = datetime.today().date()

        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 21:
            raise ValidationError('You must be at least 21 years old.')

        if len(mobile) != 10:
            raise ValidationError('Mobile should be of 10 digits.')

        return dob


    
class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ['username' , 'password']
        

class CityForm(forms.ModelForm):
    

    class Meta:
        model = CityModel  
        fields = ['city']

    def clean_dob(self):
        city = self.cleaned_data.get('city')
        city1 = CityModel.objects.all()
        
        for i in city1:
            if i==city:
                raise ValidationError('City Already Registered')
        return city


class DateFilterForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker-input'}))

