from django.urls import path

from .import views
from .views import add_course,edit_data



urlpatterns = [
    path('',views.index,name="index"),
    path('<int:course_id>',views.detail,name="detail"),
    path('search-courses/',views.CoursesSearchView.as_view(), name='search_courses'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-course/', views.add_course, name='add-course'),
    path('<int:course_id>/edit/', views.edit_data, name='edit_data'),
    path('subscribe/', views.subscribe, name="subscribe"),
    path('newsletter/',views.newsletter, name="newsletter"),

]