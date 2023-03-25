from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse

from django.views.generic import ListView

from .models import Course

# Create your views here.

def index(request):
    courses = Course.objects
    return render(request, 'diplomski/index.html',{'courses':courses})

def detail (request,course_id):
    course_detail = get_object_or_404(Course,pk=course_id)
    return render(request, 'diplomski/detail.html',{'course':course_detail})

class CoursesSearchView(ListView):
    model = Course
    template_name='diplomski\index.html'
    context_object_name='courses'

    def get_queryset(self):
        query=self.request.GET.get('q')
        return Course.objects.filter(summary__icontains=query).order_by()