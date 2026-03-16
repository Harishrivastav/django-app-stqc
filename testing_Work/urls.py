from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('', views.login_view, name='home'),

    path('login/', views.login_view, name='login'),

    path('register/', views.register, name='register'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('update/<int:job_id>/', views.update_progress, name='update'),
    
    path('assign_job/',views.assign_job,name='assign_job'),

    path('export/', views.export_excel, name='export_excel'),
]