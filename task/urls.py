from django.urls import path
from task import views

urlpatterns = [
    path('', views.task, name='task'),
    path('created/', views.created_task, name='task-created'),
    path('<int:task_id>/', views.task_detail, name='task-detail'),
]
