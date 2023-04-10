from django import forms
from .models import Course
from tinymce.widgets import TinyMCE

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class NewsletterForm(forms.Form):
    subject = forms.CharField()
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label="Email content")
