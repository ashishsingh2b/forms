from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .forms import SignupForm,EditUserForm,EditAdminForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User


# Create your views here.

def home(request):
  return render(request,'enroll/index.html')

def sign_up(request):
    if request.method == "POST":
     fm =SignupForm(request.POST)
     if fm.is_valid():
      messages.success(request,'Account Created Successfully')
      fm.save()
    else:
     fm = SignupForm()
    return render(request,'enroll/signup.html',{'form':fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
             uname = fm.cleaned_data['username']
             upass = fm.cleaned_data['password']
             user = authenticate(username=uname,password=upass)
             if user is not None:
                login(request,user)
                messages.success(request,'Log in Successfully')
                return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request,'enroll/userlogin.html',{'form':fm})
    else:
     return HttpResponseRedirect('/profile/')

def user_profile(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:  # Check if the user is a superuser (admin)
            if request.method == "POST":
                fm = EditAdminForm(request.POST, instance=request.user)
                users = User.objects.all()
                if fm.is_valid():
                    messages.success(request, "Profile updated")
                    fm.save()
            else:
                fm = EditAdminForm(instance=request.user)
                users = User.objects.all()
        else:
            if request.method == "POST":
                fm = EditUserForm(request.POST, instance=request.user)
                if fm.is_valid():
                    messages.success(request, "Profile updated")
                    fm.save()
            else:
                fm = EditUserForm(instance=request.user)
            users = None

        return render(request, 'enroll/profile.html', {'name': request.user.username, 'form': fm, 'users': users})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/login/')
def Changepass(request):
 if request.user.is_authenticated:
  if request.method =="POST":
    fm=PasswordChangeForm(user=request.user,data=request.POST)
    if fm.is_valid():
      fm.save()
      update_session_auth_hash(request, fm.user)
      messages.success(request,"Password Change Sucessfully")
      return HttpResponseRedirect('/profile/')
  else:
    fm =PasswordChangeForm(user=request)
  return render(request,'enroll/changepass.html',{'form':fm})
 else:
   return HttpResponseRedirect('/login/')
 

def Passchange(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            fm=SetPasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
             fm.save()
            update_session_auth_hash(request, fm.user)
            messages.success(request,"Password Change Sucessfully")
            return HttpResponseRedirect('/profile/')
        else:
            fm =SetPasswordForm(user=request)
        return render(request,'enroll/changepass.html',{'form':fm})
    else:
     return HttpResponseRedirect('/login/')
    
def userdetail(request,id):
    if request.user.is_authenticated:
     pi = User.objects.get(pk=id)
     fm = EditAdminForm(instance=pi)
     return render(request,'enroll/userdetails.html',{'form':fm})
    else:
       return HttpResponseRedirect('/login/')