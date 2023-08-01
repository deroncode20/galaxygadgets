from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.db.models import Q
from .forms import LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user and create an account
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            username = email.split('@')[0] 
            user.username = username # Get the user object but don't save it yet
            password = form.cleaned_data['password']  # Get the password from the form
            user.set_password(password)  # Set the password using Django's set_password method
            user.save()  # Save the user object with the hashed password

            # Optionally, you can log in the user after registration
            # (You'll need to import the login function from django.contrib.auth)
            # login(request, user)

            # Redirect to a success page or any other page you like
            return redirect('dashboard')  # Replace 'success_url_name' with your success page URL name
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def dashboard(request):
    return render(request,'accounts/dashboard.html')



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate using only the email field
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                # Redirect to the home page or any other page you want after successful login
                return redirect('dashboard')  # Replace 'dashboard' with your desired URL name
            else:
                # Invalid credentials, show an error message or handle it as you prefer
                error_message = "Invalid email or password. Please try again."
                return render(request, 'accounts/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    # Redirect to the home page or any other page you want after logout
    return redirect('Homepage')
