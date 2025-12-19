from .views import home,register,login,dashboard,task,work,sales,expenses,sales_and_expenses_page
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('home/<uuid:userid>/', home, name='home_with_id'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/<uuid:userid>/', dashboard, name='dashboard_with_id'),
    path('task/', task, name='task'),
    path('task/<uuid:userid>/', task, name='task_with_id'),
    path('work/', work, name='work'),
    path('work/<uuid:userid>/', work, name='work_with_id'),
    path('sales_and_expenses/<uuid:userid>/', sales_and_expenses_page, name='sales_and_expenses'),
    path('sales/<uuid:userid>/', sales, name='sales_with_id'),
    path('expenses/<uuid:userid>/', expenses, name='expenses_with_id'),
]