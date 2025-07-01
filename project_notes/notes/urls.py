"""
URL configuration for project_notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/store/', views.store, name='store'),

    path('login/', views.login, name='login'),
    path('login_check/', views.login_check, name='login_check'),
    path('logout/', views.logout, name='logout'),

    path('index/', views.index, name='index'),

    path('feedback/', views.feedback, name='feedback'),

    path('feedback/store/', views.feedback_store, name='feedback_store'),

    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('note/create/', views.create_note, name='create_note'),
    path('note/update/<int:pk>/', views.update_note, name='update_note'),
    path('note/delete/<int:pk>/', views.delete_note, name='delete_note'),
    path("note/<int:pk>/download/", views.download_note, name="download_note"),

    path('search/', views.search_notes, name='search_notes'),

    path('generate_note/', views.generate_note, name='generate_note'),

    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_password/', views.update_password, name='update_password'),

    path("note/send/<int:pk>/", views.send_note, name="send_note"),
    path("inbox/", views.inbox, name="inbox"),
    path("sent-notes/", views.sent_notes, name="sent_notes"),
    path("received-note/<int:pk>/", views.view_received_note, name="view_received_note"),
    path("delete-received-note/<int:pk>/", views.delete_received_note, name="delete_received_note"),

    path("note/send/<int:pk>/", views.send_note, name="send_note"),
    path("note/send-to/<int:pk>/", views.send_note_page, name="send_note_page"),
]
