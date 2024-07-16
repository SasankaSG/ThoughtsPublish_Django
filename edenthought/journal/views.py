from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm, ThoughtForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Thought, Profile
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def homepage(request):
    return render(request, 'journal/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            #user profile update content else directly form.save()
            currentUser = form.save(commit=False)
            form.save()
        #sending mails when registered: (subject, body, from address, to address)
            send_mail("Welcome to Edenthought!!", "Congratulations on creating your account", settings.DEFAULT_FROM_EMAIL, [currentUser.email] )
            #asssign the user just created to a current user
            #under profile object, we cam see user is paul who just registered himself
    
            profile = Profile.objects.create(user=currentUser)

            messages.success(request, "User Registered!")
            return redirect('my-login')
    
    context = {'RegistrationForm' : form} 
    return render(request, 'journal/register.html', context)

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            
    context = {'LoginForm' : form}   

    return render(request, 'journal/my-login.html', context)

def user_logout(request):
    auth.logout(request)
    return redirect("")

@login_required(login_url='my-login')
def dashboard(request):
    profile_pic = Profile.objects.get(user=request.user)
    context = {'ProfilePic' : profile_pic }
    return render(request, 'journal/dashboard.html', context)

@login_required(login_url='my-login')
def create_thought(request):
    form  = ThoughtForm()
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)  
            #want to post the data but wait to commit to the database
            thought.user = request.user #assigning user attribute based on the request being made
            #after thought been posted user value will be assigned
            thought.save()

            return redirect('dashboard')
    context = {'CreateThoughtForm' : form}

    return render(request, 'journal/create-thought.html', context)

@login_required(login_url='my-login')
def my_thoughts(request):
    current_user = request.user.id
    thought = Thought.objects.all().filter(user=current_user)
    context = {'AllThoughts' : thought}
    return render(request, 'journal/my-thoughts.html', context)


@login_required(login_url='my-login')
def update_thought(request, pk):
    try:
        thought = Thought.objects.get(id=pk, user=request.user)
    except:        
        return redirect('my-thoughts')
    
    form = ThoughtForm(instance=thought)
    if request.method == 'POST':
        form = ThoughtForm(request.POST, instance=thought)
        #grab the instance and anything new we add, 
        # send a post request to update the data
        if form.is_valid():
            form.save()
            return redirect('my-thoughts')
    
    context = {'UpdateThought' : form}
    return render(request, 'journal/update-thought.html', context)

@login_required(login_url='my-login')
def delete_thought(request, pk):
    try:
        thought = Thought.objects.get(id=pk, user=request.user)
    except:        
        return redirect('my-thoughts')
    if request.method == 'POST':
        thought.delete()
        return redirect('my-thoughts')        

    return render(request, 'journal/delete-thought.html')

@login_required(login_url='my-login')
def profile_management(request):
    form = UpdateUserForm(instance=request.user) #if we dont use inst, it wil come up with blank form
    profile = Profile.objects.get(user=request.user)
    form_2 = UpdateProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        #allows to update files
        form_2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
        if form_2.is_valid():
            form_2.save()
            return redirect('dashboard')
    context = {'ProfileManageForm' : form, 'ProfilePictureUpdate' : form_2}
    return render(request, 'journal/profile-management.html', context)

    
@login_required(login_url='my-login')
def delete_profile(request):
    if request.method == 'POST':
        deleteUser = User.objects.get(username=request.user)
        deleteUser.delete()
        return redirect("")        

    return render(request, 'journal/delete-profile.html')




