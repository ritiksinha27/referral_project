from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, UserStructure
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
def home(request):
    return render(request, 'home.html')
def home_str(request,cust_str):
    if CustomUser.objects.filter(unique_id=cust_str).exists():
        return redirect('ref_register',cust_str)
    
    return redirect('home')
def user_login(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        authenticated_user = authenticate(username=username, password=password)
        print(authenticated_user,username,password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('user_dash')
    return render(request, 'user_login.html')
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='user_login')
def user_dashboard(request):
    user_structure = UserStructure.objects.get(user_id=request.user)
    data={
        'user_structure':user_structure
    }
    return render(request, 'user_dash.html',data)
class user_register(View):
    def get(self, request,ref_id=None, *args, **kwargs):
        print(ref_id)
        user=request.user
        if user.is_authenticated:
            logout(request)
        if ref_id:
            ref_user=CustomUser.objects.filter(unique_id=ref_id)
            if ref_user.exists():
                return render(request, 'user_register.html',{'ref_user':ref_user.last()})
            else:
                return redirect('home')
        return render(request, 'user_register.html')
    def post(self, request,ref_id=None, *args, **kwargs):
        username= request.POST.get('username')
        password= request.POST.get('password')
        email= request.POST.get('email', None)
        mobile_no= request.POST.get('mobile_no')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        if username:
            user_crt=CustomUser.objects.create_user(username=username, password=password, email=email, mobile_no=mobile_no, first_name=first_name, last_name=last_name)
            if ref_id:
                ref_user=get_object_or_404(CustomUser, unique_id=ref_id)
                UserStructure.objects.create(user_id=user_crt, ref_by_user_id=ref_user)
                ref_usr_str=UserStructure.objects.get(user_id=ref_user)
                ref_usr_str.child_branch.add(user_crt)
            else:
                UserStructure.objects.create(user_id=user_crt)
            login(request, CustomUser.objects.get(username=username))
            return redirect('user_dash')
        else:
            return render(request, 'user_register.html')


def admin_login(request):
    user=request.user
    if user.is_authenticated and user.groups.filter(name='admin').exists():
        return redirect('admin_dash')
    elif user.is_authenticated:
        logout(request)
        return redirect('admin_login')
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        authenticated_user = authenticate(username=username, password=password)
        print(authenticated_user,username,password)
        if authenticated_user is not None and authenticated_user.groups.filter(name='admin').exists():
            login(request, authenticated_user)
            return redirect('admin_dash')
    return render(request, 'admin_login.html')
@login_required(login_url='admin_login')
def admin_dash(request):
    user=request.user
    if user.groups.filter(name='admin').exists():
        pass
    else:
        messages.error(request, 'You are not admin')
        return redirect('admin_login')
    all_str=UserStructure.objects.filter(user_id__is_superuser=False).order_by('-id')
    data={
        'all_str':all_str,
        'total_count':all_str.count()
    }
    return render(request, 'admin_dash.html',data)

def add_points(request,usr_str_id):
    usr_str=UserStructure.objects.get(id=usr_str_id)
    if request.method == 'POST':
        points= request.POST.get('points')
        usr_str.points+=int(points)
        usr_str.save()
        return redirect('admin_dash')
    

def username_validate(request, usr_name):
    usern = CustomUser.objects.filter(username=usr_name).exists()
    if usern:
        return JsonResponse({'is_valid': False})
    else:
        return JsonResponse({'is_valid': True})

def mobile_validate(request, mob_no):
    mob = CustomUser.objects.filter(mobile_no=mob_no).exists()
    if mob:
        return JsonResponse({'is_valid': False})
    else:
        return JsonResponse({'is_valid': True})

def delete_user(request,usr_id):
    user=CustomUser.objects.get(id=usr_id)
    if user.groups.filter(name='admin').exists():
        return redirect('admin_dash')
    user.delete()
    return redirect('admin_dash')