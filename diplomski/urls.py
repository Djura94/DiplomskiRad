from django.urls import path

from .import views


urlpatterns = [
    path('',views.index,name="index"),
    path('<int:course_id>',views.detail,name="detail"),
    path('search-courses/',views.CoursesSearchView.as_view(), name='search_courses'),


]