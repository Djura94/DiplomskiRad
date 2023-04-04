from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    courses = Course.objects
    return render(request, 'diplomski/index.html',{'courses':courses})

def detail (request,course_id):
    course_detail = get_object_or_404(Course,pk=course_id)
    return render(request, 'diplomski/detail.html',{'course':course_detail})

#Search
class CoursesSearchView(ListView):
    model = Course
    template_name='diplomski/index.html'
    context_object_name='courses'

    def get_queryset(self):
        query=self.request.GET.get('q')
        return Course.objects.filter(summary__icontains=query).order_by()


#Login/Logout
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'diplomski/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'diplomski/login.html')
def logout_view(request):
    logout(request)
    return redirect('index')
 
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CourseForm()
    
    context = {
        'form': form
    }
    return render(request, 'diplomski/add_course.html', context)

def edit_data(request, course_id):
    # Retrieve the course object from the database
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        # Process the form data if it is a POST request
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        # Render the edit form if it is a GET request
        form = CourseForm(instance=course)
    
    # Render the template with the form and course objects
    return render(request, 'diplomski/edit_data.html', {'form': form, 'course': course})
