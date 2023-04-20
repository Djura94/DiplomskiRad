from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from django.views.generic import ListView
from .models import Course, SubscribedUsers
from .decorators import user_is_superuser
from .forms import CourseForm, NewsletterForm
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings
import os

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
            return render(request, 'diplomski/login.html', {'error': 'Pogrešan username ili šifra.'})
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

def subscribe(request):
    if request.method =='POST':
        name = request.POST.get('name',None)
        email =request.POST.get('email',None)

        if not name or not email:
            messages.error(request,"Morate unijeti korektne podatke da bi se pretplatili na Newsletter")
            return redirect('index')
        
        if get_user_model().objects.filter(email=email).first():
            messages.error(request,f"Već postoji korisnik sa ovim mejlom.")
            return redirect(request.META.get("HTTP_REFERER",'index'))
        
        subscribe_user=SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request,f"{email} email adresa vec postoji.")
            return redirect(request.META.get("HTTP_REFERER",'index'))
        
        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('index')
        
        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.name=name
        subscribe_model_instance.email=email
        subscribe_model_instance.save()
        messages.success(request,f'{email} Uspješno ste se prijavili na moj newsletter')
        return redirect(request.META.get("HTTP_REFERER",'index'))

@user_is_superuser
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')

            # Include the unsubscribe hyperlink in the email content for each receiver
            for receiver in receivers:
                # Get the unsubscribe URL for each receiver
                unsubscribe_url = request.build_absolute_uri(reverse('unsubscribe', args=[receiver]))

                # Include the unsubscribe hyperlink in the email content
                email_message_with_unsubscribe = f"{email_message}\n\nDa se ispišete sa newslettera, kliknite na sljedeci link: {unsubscribe_url}"

                mail = EmailMessage(subject, email_message_with_unsubscribe, f"<{request.user.email}>", [receiver])
                mail.content_subtype = 'html'
                if mail.send():
                    messages.success(request, f"Email uspješno poslat na {receiver}")
                else:
                    messages.error(request, f"Greška pri slanju email-a na {receiver}")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

        return redirect('index')

    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request=request, template_name='diplomski/newsletter.html', context={'form': form})



def unsubscribe(request, email):
    try:
        subscriber = SubscribedUsers.objects.get(email=email)
        # Remove the subscriber from the database
        subscriber.delete()
        # Redirect to a success page or display a success message
        return render(request, 'diplomski/unsubscribe_success.html')
    except SubscribedUsers.DoesNotExist:
        # Handle case when subscriber is not found
        return render(request, 'diplomski/unsubscribe_error.html')


def download_cv(request):
    cv_file_path = os.path.join(settings.STATIC_ROOT, 'FilipDjuricCV.pdf')  # Path to your CV file
    with open(cv_file_path, 'rb') as cv_file:
        response = HttpResponse(cv_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="FilipDjuricCV.pdf"'
        return response