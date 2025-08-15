from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about_us, name="about"),
    path("contact/", views.contact_us, name="contact"),
    path("events/", views.our_events, name="events"),
    path("facility/", views.our_facility, name="facility"),
    path("principal/", views.our_principal, name="principal"),
    path("teachers/", views.our_teachers, name="teacher"),
    path("course-cse/", views.cse, name="cse"),
    path("course-ece/", views.ece, name="ece"),
    path("course-ice/", views.ice, name="ice"),

    # Student URLs
    path("student-registration/", views.student_signup, name="student_signup"),
    path("student-login/", views.student_login, name="student_login"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student-logout/", views.student_logout, name="student_logout"),
    path('student-profile/', views.Student_profile, name='student_profile'), 
    
    # Teacher URLs
    path("institute-signup/", views.teacher_signup, name="teacher_signup"),
    path("institute-login/", views.teacher_login, name="teacher_login"),
    path("institute-logout/", views.teacher_logout, name="teacher_logout"),
    path('institute-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('profile/', views.teacher_profile, name='teacher_profile'), 
    path('change-password/', views.change_password, name='change_password'),
    path('update/<int:id>/', views.update_content, name='update_content'),
    path('delete/<int:id>/', views.delete_content, name='delete_content'),
    
    # library URLs
    path("library-book-details/", views.book_details, name="book_details"),
    path('update-book-details/<int:id>/', views.update_book_details, name='update_book_details'),
    path('delete-book-details/<int:id>/', views.delete_book_details, name='delete_book_details'),
    path("library-book-status/", views.book_status, name="book_status"),
    path('update-book-status/<int:id>/', views.update_book_status, name='update_book_status'),
    path('delete-book-status/<int:id>/', views.delete_book_status, name='delete_book_status'),
    path("library-book-issue/", views.book_issue, name="book_issue"),
    path('update-book-issue/<int:id>/', views.update_book_issue, name='update_book_issue'),
    path('delete-book-issue/<int:id>/', views.delete_book_issue, name='delete_book_issue'),
]
