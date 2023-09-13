from django.shortcuts import render ,HttpResponse , redirect , HttpResponseRedirect
from .forms import RegisterForm , CityForm
from .models import RegisterModel ,CityModel
from django.db.models import Q
import csv
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import  csv

from collections import Counter
from django.db.models import F

from django.core.exceptions import ValidationError

# Create your views here.
@login_required
def username_context(request):
    return {'username': request.user.username}

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dash')  # Replace 'home' with the name of your home URL
        else:
            error_message = 'Invalid username or password'  # Customize the error message as needed
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

    
    
# user logout view

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')



@login_required
def UserRegister(request):
    if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
    else:
        form = RegisterForm()
    cities = CityModel.objects.all()
    return render(request, 'register.html', {'form': form , 'cities' : cities })

def city(request):
    city = CityModel.objects.all()
    data = CityModel.objects.all().order_by('-id')
    paginator = Paginator(data, 10)  
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)

    return render(request, 'city.html', {'city' : city , 'data':data })


def add_city(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = request.POST.get('city')
            
            form.save()
            return redirect('home')
    else:
        form = CityForm()
    cities = CityModel.objects.all()
    
  
    return render(request, 'cityReg.html', {'form': form , 'cities' : cities } )

@login_required
def home(request):
    data = RegisterModel.objects.all().order_by('-id')
    search = request.GET.get('search')
    date = request.GET.get('date')
    status_select = request.GET.get('status_select')
    citySearch = request.GET.get('citySearch')
    
 
    if search:
        data = data.filter(
            Q(name__icontains=search) |
            Q(mobile__icontains=search)
        )
    elif date:
        data = data.filter(
            Q(doj__icontains=date)
        )
    elif status_select:
        data =data.filter(
            Q(status__icontains=status_select)
        )
    elif citySearch:
        data =data.filter(
            Q(cityReg__id__icontains=citySearch)
        )
        
 
        
    paginator = Paginator(data, 10)  
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    city = CityModel.objects.all()
    return render(request, 'home.html', {'data': data , 'city' : city})



@login_required
def update_user(request, id):
    uid = RegisterModel.objects.get(pk=id)
 
    
    if request.method == 'POST':
        uid = RegisterModel.objects.get(pk=id)
        form = RegisterForm(request.POST,request.FILES, instance=uid)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm(instance=uid)
    cities = CityModel.objects.all()
    context = {
        'form': form,
        'cities' : cities,
       
    }
    return render(request, 'update2.html', context)


    # return render(request, 'update.html', {'form': form })
    
class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

@login_required
def export_data(request):
    data = RegisterModel.objects.all()
    model_fields = RegisterModel._meta.fields
    excluded_fields = ['pwd']
    field_names = [field.name for field in model_fields if field.name not in excluded_fields]

    rows = ([getattr(row, field_name) for field_name in field_names] for row in data)
    rows = list(rows)  # Convert generator object to a list

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)

    response = StreamingHttpResponse(
        (writer.writerow(row) for row in [field_names] + rows),  
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    return response

def import_page(request):
    return render(request , 'import.html')

@login_required           
def import_data(request):
    if request.method == 'POST':
        csvfile = request.FILES['import']
        decoded_file = csvfile.read().decode('utf-8').splitlines()

        reader = csv.DictReader(decoded_file)
        def parse_date(date_str):
            if date_str:
                date_obj  =  datetime.strptime(date_str, '%m/%d/%Y') 
                
                return date_obj.strftime('%Y-%m-%d')
            return None
        
        c= 1
        rows = ""
        error_message = None
        
        
        for row in reader:
            c +=1
            name = row['name']
            mobile = row['mobile']
            if RegisterModel.objects.filter(mobile=mobile).exists():
                error_message = "Mobile number already exists."
                rows = "Error at row : " + str(c)
            email = row['email']
            doj = parse_date(row['doj']) if row['doj'] else None
            picture = row['picture']
            dob = parse_date(row['dob']) if row['dob'] else None
            
            # Check if the dob is valid and the person is at least 21 years old
            if dob:
                dob_date = datetime.strptime(dob, '%Y-%m-%d')
                today = datetime.today()
                age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
                if age < 21:
                    error_message = "Age must be at least 21 years."
                    rows = "Error at row : " + str(c)
            
            status = row['status']
            c4 = row['c4']
            sign_off = row['sign_off']
            accNnum = row['accNnum']
            ifsc = row['ifsc']
            aadhar = row['aadhar']
            aadharAttested = row['aadharAttested']
            cityReg = row['cityReg']
            designation = row['designation']
            programEnroll = row['programEnroll']
            code = row['code']
            
            if RegisterModel.objects.filter(code=code).exists():
                error_message = "Code already exists." 
                rows= "Row : " +str(c)

          
                
            try:
                city_instance = CityModel.objects.get(city=cityReg)
            except CityModel.DoesNotExist:
                city_instance = CityModel(city=cityReg)
                city_instance.save()
            
            
            
            c4Date = parse_date(row['c4Date']) if row['c4Date'] else None
            c4Exp = row['c4Exp']
            if not c4Exp:
                c4Exp = 0
            else:
                c4Exp = int(c4Exp)
            
            dol = parse_date(row['dob']) if row['dob'] else None
            if error_message:
                return render(request, 'import.html', {'error_message': error_message , 'rows' : rows})
            
     
                
            RegisterModel.objects.create(
                    name=name, email=email, mobile=mobile, doj=doj, picture=picture, dob=dob,
                    c4=c4, sign_off=sign_off, accNnum=accNnum, ifsc=ifsc,
                    status=status, aadhar=aadhar, aadharAttested=aadharAttested,
                    cityReg=city_instance, designation=designation,
                    programEnroll=programEnroll, code=code, c4Date=c4Date, c4Exp=c4Exp,dol=dol)
        
    return redirect('home')



def dash(request):
    
    
    users = RegisterModel.objects.all()
    count = users.count()
    
    
    designation_counter = Counter(u.designation for u in users)
    status_counter = Counter(u.status for u in users)
    program_counter = Counter(u.programEnroll for u in users)
    
    cFWP = designation_counter['FWP']
    cSUP = designation_counter['Supervisor']
    cCM = designation_counter['City Manager']
    cWE = designation_counter['Warehouse Executive']
    tDes = cFWP + cSUP + cCM + cWE

    cW = status_counter['Working']
    cNW = status_counter['Not Working']
    cUE = status_counter['Under Evaluation']
    cSIP = status_counter['Selection In Process']
    cRe = status_counter['Rejected']
    cSe = status_counter['Selected']
    tStatus = cW + cNW + cUE+cSIP +cRe + cSe

    cMI = program_counter['MI']
    cNOW = program_counter['NOW']
    cLAMPS = program_counter['LAMPS']
    tpro = cMI + cLAMPS + cNOW
    
    
    context = {
        'cFWP': cFWP,
        'cSUP': cSUP,
        'cCM': cCM,
        'cWE': cWE,
        'cW': cW,
        'cNW': cNW,
        'cUE': cUE,
        'cSIP': cSIP,
        'cRe': cRe,
        'cSe': cSe,
        'cLAMPS' : cLAMPS,
        'cMI' : cMI,
        'cNOW' : cNOW,
        'tDes' : tDes,
        'tStatus' : tStatus,
        'tpro' : tpro,
        'count' : count
        
    }
    return render(request, 'dash.html', context)



