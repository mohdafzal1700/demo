from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as loginauth ,logout as logoutauth,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# Create your views here


#################################################################################

def sig(request):
  if request.user.is_authenticated:
         return redirect('home')
  if request.POST:
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        if User.objects.filter(username=username).exists():
           messages.warning (request ,'username exist')
           return redirect('signin')
        
        if User.objects.filter(email=email).exists():
           messages.warning (request, 'email exists')
           return redirect ('signin')
        
        if len(password1)<8:
           messages.warning(request,'Password must be greater than 8 characters')
           return redirect ('signin')
        if password1!=password2:
           messages.warning(request,'password not match')
           return redirect('signin')
        
           
        user=User.objects.create_user(username,email,password1)
        user.save()
        return redirect('login')
     
     
  return render (request,'sigin.html')
#################################signin end############################################


#################################login#################################################
@never_cache
def login(request):
   
   error_message=None
   if request.user.is_authenticated:
      return redirect('home')
   
   if request.POST:
      username=request.POST['username']
      password=request.POST['password']
      user=authenticate(username=username,password=password)
      
      if user:
         loginauth(request,user)
         return redirect('home')
      else:
         error_message='invalid username or password'
         
   return render (request,'login.html',{'error_message':error_message})
   
#################################login end#############################################


#################################home##################################################
@never_cache
@login_required(login_url='login')
def home(request):
   if request.user.is_authenticated:
      if request.user.is_superuser:
         return redirect('admin1')
   
   
      return render (request,'home.html',{'user':request.user})
   return redirect('login')

#################################home end###############################################

#################################myadmin################################################
@never_cache
@login_required(login_url='login')
def myadmin(request):
   if request.user.is_superuser:
       user=User.objects.all().order_by('-date_joined')
       return render (request,'admin.html',{'users':user})
   return redirect('login')
#################################myadmin end############################################

#################################logout#################################################
@login_required(login_url='/')
def logout(request):
   logoutauth(request)
   
   return redirect(login)
################################# end logout ################################################

#################################edit################################################
@login_required(login_url='/')
def edituser(request,id):
   user=get_object_or_404(User,id=id)
   if request.POST:
      name= request.POST.get('username')
      email= request.POST.get('email')
      
      # if User.objects.filter(username=name).exists():
      #    messages.warning(request,'already exists')
      #    return redirect('admin1')
      
      # if User.objects.filter(email=email).exists():
      #    messages.warning(request,'already exists')
      #    return redirect ('admin1')
      try:
         user.username=name
         user.email=email
         user.save()
      except Exception as e:
         print(e)
         messages.warning(request,"user already exist")
         
         
      
      return redirect('admin1')
    
#################################end edit################################################

#################################delete################################################
@login_required(login_url='/')
def delete(request,id):
  if request.POST:
        del_user = User.objects.get(id=id)
        del_user.delete()

  return redirect(myadmin)


#################################search################################################
@login_required(login_url='/')
def searchuser(request):
     if request.POST:
        detail_user=request.POST['search']
        if detail_user:
           user=User.objects.filter(username=detail_user).order_by('username')
        else:
           user=User.objects.all()
           
        return render (request,'admin.html',{'users':user})
        
      
#################################end search##########################################

#################################add user############################################
@login_required(login_url='/')
def aadduser(request):
   if request.POST:
        name=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if User.objects.filter(username=name).exists():
            messages.warning(request,'Username exists')
            return redirect('admin1')
        
        if User.objects.filter(email=email).exists():
            messages.warning(request,'Email exists')
            return redirect('admin1')
        
        if len(password1)<8:
            messages.warning(request,'Password must be greater than 8 characters')
            return redirect('admin1')
        
        if password1!=password2:
            messages.warning(request,'Passwords do not match')
            return redirect('admin1')
        
        
        user=User.objects.create_user(username=name,email=email,password=password1)
        user.save()
        return redirect('admin1')
   return render(request,'admin.html')     
        
   

#################################end adduser#########################################

