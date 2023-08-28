from django.urls import path
from .views import login_view ,dash ,logout_user ,import_page, UserRegister , city , home, import_data ,update_user,export_data,add_city
urlpatterns = [
    path('' , login_view, name= 'login'),
    path('logout/' , logout_user, name= 'logout'),
    path('register/' , UserRegister , name = 'register'),
    path('home/' , home , name = 'home'),
    path('update/<int:id>/', update_user, name='update_user'),
    path('import_page/', import_page, name='import_page'),
    path('import/', import_data, name='import_data'),
    path('export/', export_data, name='export_data'),
    path('city/' , city , name = 'city'),
    path('add_city/' , add_city , name = 'add_city'),
    path('dash/' ,dash , name= 'dash'),
    
  
]
