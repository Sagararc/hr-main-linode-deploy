from django.db import models
from datetime import datetime, timedelta ,date
# Create your models here.
status_choices = (
    ('Working' , 'Working'),
    ('Not Working' , 'Not Working'),
    ('Under Evaluation' , 'Under Evaluation' ) , 
    ('Selection In Process' , 'Selection In Process') , 
    ('Rejected' , 'Rejected') , 
    ('Selected' , 'Selected')
    
)

    
class CityModel(models.Model):
    city = models.CharField(max_length=30 , unique=True)
    
    def __str__(self):
        return self.city
    
class RegisterModel(models.Model):
    name = models.CharField(max_length=100 , null=True)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    doj = models.DateField( null=True,blank=True)
    picture = models.ImageField(upload_to='images/',null=True, default="",blank=True)
    dob = models.DateField(null=True,blank=True)
    status = models.CharField(choices=status_choices ,blank=True, default='' ,null=True, max_length=20)
    c4 =  models.ImageField(upload_to='c4/' , default="" , null=True,blank=True)
    sign_off= models.ImageField(upload_to='sign_off/' , null=True,default="" ,blank=True)
    accNnum = models.CharField(max_length=30 , default='',null=True, blank=True)
    ifsc = models.CharField(max_length=30 , default='', null=True,blank=True)
    aadhar = models.ImageField(upload_to = 'aadhar/' ,default='' ,null=True, blank=True )
    aadharAttested = models.ImageField(upload_to = 'aadhar_attested/' ,default='' , blank=True )
    cityReg = models.ForeignKey(CityModel , on_delete=models.CASCADE , default='') 
    designation = models.CharField(max_length=20 ,default='' , null=True,blank=True )
    programEnroll = models.CharField(max_length=30 , default='' , null=True,blank=True)
    code = models.CharField(max_length=30, default='' , null=True,blank=True)
    c4Date = models.DateField( null=True,blank=True)
    c4Exp = models.IntegerField(default='365' , null='True' ,blank=True )
    dol = models.DateField(null=True,blank=True)
    
    def __str__(self):
            return self.name

class UserLogin(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
