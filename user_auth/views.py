from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.views.generic import ListView
from django.contrib import messages

# modules needed for user authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# importing the use model
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'index.html')

class RegisterUser(ListView):
    form = RegisterForm
    template_name = 'register.html'

    def get(self, request):
        context = {
            'form': self.form()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        #passing the form data to instantiate the usercreation
        form = self.form(request.POST, request.FILES) 
        if form.is_valid():
            user = form.save()
            
            messages.success(request, 'sucessfully created account')
            return redirect('home')

        #adding is-invalid class to all form field that is invalid
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'

        # adding is-valid class to all valid form field
        valid_fields = list(filter(lambda i: i not in form.errors, list(form.fields.keys()) ))
        for field in valid_fields:
            form[field].field.widget.attrs['class'] += ' is-valid'

        return render(request, self.template_name, {'form': form})

class LoginUser(ListView):
    form = LoginForm
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            username = User.objects.filter(email = form.cleaned_data.get('email')).first()
            user = authenticate(username=username, password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                messages.success(request, f'successfully logged in as {user.username}')
                return redirect('/')
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, self.template_name, {'form': form})
        else:
            #adding is-invalid class to all form field that is invalid
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            return render(request, self.template_name, {'form': form})


@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'successfully logged out')
        return redirect('/')

@login_required
def profile(request):
    return render(request, 'profile.html')
