from .views import (
    home,register,login,dashboard,task,work,sales,expenses,cashbook,update_rma_status,update_work_status,
    sales_and_expenses_page,rma,attendance_view,attendance_submit,logout,home_view,apply_leave
)
from django.urls import path

urlpatterns = [
    path('', home_view, name='home'),
    path('home/<uuid:userid>/', home_view, name='home_with_id'),
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
    path('cashbook/<uuid:userid>/', cashbook, name='cashbook_with_id'),
    path('rma/<uuid:userid>/', rma, name='rma'),
    path('attendance/<uuid:userid>/', attendance_view, name='attendance'),
    path('attendance_submit/<uuid:userid>/', attendance_submit, name='attendance_submit'),
    path('leave/apply/<uuid:userid>/', apply_leave, name='apply_leave'),
    path('update_rma/<uuid:userid>/', update_rma_status, name='update_rma'),
    path('update_work/<uuid:userid>/', update_work_status, name='update_work'),
    path('logout/', logout, name='logout'),
]