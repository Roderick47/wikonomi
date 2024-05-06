from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from Profile.models import Profile
from urllib.parse import urlencode
from django.urls import reverse
from Business.models import Business
from Follow.models import ProductSubscription


from .forms import SignUpForm,UserForm,ProfileForm


# Create your views here.

#Signs up a user
def SignupView(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            username= form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            authuser = authenticate(username=username,password=raw_password)
            login(request,authuser)
            return redirect('Home:home')
    else:
        form = SignUpForm()
    return render(request,'Profile/signup.html',{'form':form})

from django.views.generic import View


#Logs in a user
def LoginView(request):
    if request.user.is_authenticated:
        return redirect('Home:home')
    if request.method=="POST":
        next_url = request.GET.get('next')
        form=AuthenticationForm(request.POST)
        formusername = request.POST['username']
        formpassword = request.POST['password']
        user = authenticate(username=formusername, password=formpassword)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url) 
            return redirect('Home:home')
        else:
            if next_url:
                base_url = reverse("Profile:login")
                next = urlencode({"next":next_url})
                url = '{}?{}'.format(base_url,next)
                return redirect(url)
            return redirect('Profile:login')
    form=AuthenticationForm()
    return render(request, "Profile/login.html",{'form':form})

#logs out a user
def LogoutView(request):
        logout(request)
        return redirect('Home:home')

#returns the profile page of a logged in user.
def ProfileView(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        prof_bus = Business.objects.filter(author=request.user)
        MySubscriptions = ProductSubscription.objects.filter(user=request.user)


        return render(request,'Profile/profile.html',{'profile':profile,'all_business':prof_bus,'MySubscriptions':MySubscriptions})

    return redirect('Profile:login')


def UpdateProfileView(request,prof_id):
    if not request.user.is_authenticated:
        return redirect('Profile:login')
    profile = Profile.objects.get(id=prof_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('Profile:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request,'Profile/profile_update_form.html',{'user_form':user_form,'profile_form':profile_form})

def PublicProfileView(request,user_id):
    user1 = User.objects.get(id=user_id)
    profile = Profile.objects.get(user= user1)
    return render(request,'Profile/profile.html',{'profile':profile})