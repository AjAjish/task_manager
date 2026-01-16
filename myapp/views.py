from django.shortcuts import render , redirect
from django.contrib import messages
from django.utils import timezone
from .models import User, Task , Work , SalesAndExpenses , RMA , Attendance
from django.http import JsonResponse
import json 
from datetime import datetime

today = timezone.now().date().isoformat()

# Create your views here.

def home(request,userid=None):
    userid = request.session.get('userid')
    if userid:
        return render(request, 'base.html', {'userid': userid})
    return render(request, 'base.html')

def home_view(request,userid=None)  :
    userid = request.session.get('userid')
    if userid:
        return render(request, 'home.html', {'userid': userid})
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobileNo = request.POST.get('mobileNo')
        password = (request.POST.get('password'))
        confirmPassword = (request.POST.get('confirmPassword'))  

        if password != confirmPassword:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')
        
        User.objects.create(
            username=username,
            email=email,
            mobileNo=mobileNo,
            password=password
        )

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')


    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.password == password:  
                userid = str(user.userid)
                # Make it userid on session after login
                request.session['userid'] = userid
                messages.success(request, 'Login successful!')
                return redirect('dashboard_with_id', userid=userid)
            # Check if user is admin
            elif user.role == "admin" and user.password == password:
                userid = str(user.userid)
                request.session['userid'] = userid
                messages.success(request, 'Login successful!')
                return redirect('dashboard_with_id', userid=userid)
            else:
                messages.error(request, 'Invalid username or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

def dashboard(request,userid=None):
    users = User.objects.all()
    tasks = Task.objects.all()
    works = Work.objects.all()
    rma_list = RMA.objects.all()
    attendance_list = Attendance.objects.all()
    sales_and_expenses = SalesAndExpenses.objects.all()

    userid = request.session.get('userid')
    if userid:
        return render(request, 'dashboard.html', {
            'userid': userid,
            'users': users,
            'tasks': tasks,
            'works': works,
            'rma_list': rma_list,
            'attendance_list': attendance_list,
            'slaes_and_expenses' : sales_and_expenses
        })
    return render(request, 'dashboard.html')

def task(request,userid=None):
    userid = request.session.get('userid')
    user = User.objects.get(userid=userid) if userid else None
    if userid:
        if request.method == 'POST':
            # Task details from the form
            taskName = request.POST.get('taskName')
            taskAddress = request.POST.get('taskAddress')
            taskMobile = request.POST.get('taskMobile')
            taskEmail = request.POST.get('taskEmail')

            # System data from the form
            systemType = request.POST.get('systemType')
            brand = request.POST.get('brand')
            model = request.POST.get('model')
            serial_number = request.POST.get('serial_number')
            issueDescription = request.POST.get('issueDescription')
            entryDate = request.POST.get('entryDate')
            dueDate = request.POST.get('dueDate')
            remark = request.POST.get('remark')
            charger = request.POST.get('charger')

            # Patment data from the form
            price = request.POST.get('price')
            advance = request.POST.get('advance')
            paymentStatus = request.POST.get('paymentStatus')

            remainder = int(price) -  int(advance)
            
            # Create a JSON structure for task details
            task_details = {
                'task_created_by': user.username if user else 'Unknown',
                'task_info': {
                    'taskName': taskName,
                    'taskAddress': taskAddress,
                    'taskMobile': taskMobile,
                    'taskEmail': taskEmail,
                    'taskStatus': 'Pending',
                    
                },
                'system_info': {
                    'systemType': systemType,
                    'brand': brand,
                    'model': model,
                    'serial_number': serial_number,
                    'issueDescription': issueDescription,
                    'entryDate': entryDate,
                    'dueDate': dueDate,
                    'remark': remark,
                    'charger': charger,
                },
                'payment_info': {
                    'price': price,
                    'advance': advance,
                    'paymentStatus': paymentStatus,
                    'remainderAmount': remainder,
                }
            }

            Task.objects.create(taslDetails=task_details)
            messages.success(request, "Task created successfully.")

            return render(request, 'task.html', {'userid': userid})

    return render(request, 'task.html', {'userid': userid})

def work(request,userid=None):
    userid = request.session.get('userid')

    if not userid:
        return redirect('login')  # or your login page

    users = User.objects.all()
    tasks = Task.objects.all()
    works = Work.objects.all()

    if request.method == 'POST':
        assigned_userid = request.POST.get('assignedUserId')
        work_taskid = request.POST.get('workTaskId')
        work_description = request.POST.get('workDescription')

        try:
            assigned_user = User.objects.get(userid=assigned_userid)
            assigned_task = Task.objects.get(taskid=work_taskid)

            Work.objects.create(
                workAssignedTo=assigned_user,
                workTask=assigned_task,
                workDescription=work_description
            )

            messages.success(request, "Work assigned successfully.")
            return redirect('work')

        except User.DoesNotExist:
            messages.error(request, "Selected user does not exist.")

        except Task.DoesNotExist:
            messages.error(request, "Selected task does not exist.")

        except Work.DoesNotExist:
            messages.error(request, "Work assignment failed.")
        
        except Exception as e:
            print(f"Error assigning work: {str(e)}")  # Debugging line
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'work.html', {
        'userid': userid,
        'user': users,     # keeping your template variable name
        'tasks': tasks,
        'works': works
    })

def sales_and_expenses_page(request, userid=None):
    
    userid = request.session.get('userid')
    # To show only today sales and expenses record
    sales_and_expenses = SalesAndExpenses.objects.filter(salesData__date=today).first()

    if not userid:
        return redirect('login')  # or your login page
    return render(request, 'sales.html', {'userid': userid, 'sales_and_expenses': sales_and_expenses})

def sales(request,userid=None):
    userid = request.session.get('userid')
    if not userid:
        return redirect('login')  # or your login page
     
    # Get or create today's record
    sales_obj, created = SalesAndExpenses.objects.get_or_create(
        salesData__date=today,
        defaults={
            "salesData": {
                "date": today,
                "income": [],
                "outgoing": [],
                "total_income": 0,
                "total_outgoing": 0,
                "remaining_amount": 0
            }
        }
    )

    if request.method == 'POST':
        data = sales_obj.salesData
        income_list = data.get('income', [])
        s_no = len(income_list)
        income_list.append({
            "s_no": s_no,
            "product": request.POST.get('product_name'),
            "amount": float(request.POST.get('product_amount'))
        })

        # Recalculate totals
        total_income = sum(i["amount"] for i in income_list)
        total_outgoing = sum(o["amount"] for o in data.get("outgoing", []))

        data.update({
            "income": income_list,
            "total_income": total_income,
            "remaining_amount": total_income - total_outgoing
        })

        sales_obj.salesData = data
        sales_obj.save()

        messages.success(request, "Sales data updated successfully.")
        return redirect('sales_and_expenses',userid=userid)
    
    return render(request, 'sales.html', {'userid': userid,})
    

def expenses(request, userid=None):
    userid = request.session.get('userid')
    if not userid:
        return redirect('login')  # or your login page

    # Get or create today's record
    sales_obj, created = SalesAndExpenses.objects.get_or_create(
        salesData__date=today,
        defaults={
            "salesData": {
                "date": today,
                "income": [],
                "outgoing": [],
                "total_income": 0,
                "total_outgoing": 0,
                "remaining_amount": 0
            }
        }
    )

    if request.method == "POST":
        data = sales_obj.salesData
        outgoing_list = data.get("outgoing", [])

        # Auto S No: 0 → n
        s_no = len(outgoing_list)

        outgoing_list.append({
            "s_no": s_no,
            "name": request.POST.get("expense_name"),
            "amount": float(request.POST.get("expense_amount", 0))
        })

        # Recalculate totals
        total_income = sum(i["amount"] for i in data.get("income", []))
        total_outgoing = sum(o["amount"] for o in outgoing_list)

        data.update({
            "outgoing": outgoing_list,
            "total_outgoing": total_outgoing,
            "remaining_amount": total_income - total_outgoing
        })

        sales_obj.salesData = data
        sales_obj.save()

        messages.success(request, "Expense added successfully.")
        return redirect("sales_and_expenses", userid=userid)

    return render(request, "sales.html", {"userid": userid})

def rma(request, userid=None):
    rma_list = RMA.objects.all()
    rmaData = {}
    userid = request.session.get('userid')
    if not userid:
        return redirect('login')  # or your login page
    
    for rma in rma_list:
        rma.first_detail = (
            next(iter(rma.rmaDetails.values()), {})
            if isinstance(rma.rmaDetails, dict)
            else {}
        )

    if request.method == 'POST':
        dc_no = request.POST.get('dc_no')
        to_address = request.POST.get('to_address')
        product_name = request.POST.get('product_name')
        serial_number = request.POST.get('serial_number')
        quantity = request.POST.get('quantity')
        sent_date = request.POST.get('sent_date')
        problem_description = request.POST.get('problem_description')

        rmaData = {
            'dc_no': dc_no,
            'to_address': to_address,
            'product_name': product_name,
            'serial_number': serial_number,
            'quantity': quantity,
            'sent_date': sent_date,
            'problem_description': problem_description,
            'return_status': 'Pending',
            'update_date': None
        }

        RMA.objects.create(rmaDetails=rmaData)
        messages.success(request, "RMA request submitted successfully.")
        return redirect('rma', userid=userid)

    return render(request, 'rma.html', {'userid': userid ,"rma_list": rma_list})

def attendance_view(request, userid=None):
    attendance_records = Attendance.objects.all()
    user = User.objects.get(userid=userid) if userid else None
    userid = request.session.get('userid')
    if not userid:
        return redirect('login')  # or your login page

    attendance_dict = {}
    for record in attendance_records:
        date_str = str(record.created_at.date())  # Convert date to string (YYYY-MM-DD)
        # Assuming attendanceDetails is stored as JSON field
        attendance_dict[date_str] = record.attendanceDetails
    
    return render(request, 'attendance.html', {'userid': userid , 'user': user,
                 'attendance_list': attendance_dict})

def attendance_submit(request, userid=None):
    userid = request.session.get('userid')
    if not userid:
        return redirect('login')  # or your login page
    
    if request.method == 'POST':
        try:
   
            data = json.loads(request.body)

            attendance_date = list(data.keys())[0]
            attendance_items = data[attendance_date].get('AttendanceData', [])

            current_time = timezone.localtime(timezone.now()).strftime("%H:%M:%S")

            attendance_qs = Attendance.objects.filter(attendanceDetails__has_key=attendance_date)

            if attendance_qs.exists():
                attendance_record = attendance_qs.first()
                existing_data = attendance_record.attendanceDetails.get(attendance_date, {})
                existing_items = existing_data.get('AttendanceData', [])

                # Existing user names
                existing_names = {item['name'] for item in existing_items}

                new_items = []

                for item in attendance_items:
                    if item['name'] in existing_names:
                        messages.error(request, f"Attendance already submitted for {item['name']}.")
                        return JsonResponse({
                            "success": True,
                        }, status=400)

                    item['submitted_time'] = current_time
                    item.setdefault('leave',None)
                    new_items.append(item)

                existing_items.extend(new_items)

                attendance_record.attendanceDetails[attendance_date]['AttendanceData'] = existing_items
                attendance_record.save()

                messages.success(request, "Attendance submitted successfully.")
                return JsonResponse({
                    "success": True
                })

            else:
                # First submission for the date
                for item in attendance_items:
                    item['submitted_time'] = current_time
                    item.setdefault('leave',None)

                attendance_data = {
                    attendance_date: {
                        'AttendanceData': attendance_items,
                    }
                }

                Attendance.objects.create(attendanceDetails=attendance_data)
                messages.success(request, "Attendance submitted successfully.")
                return JsonResponse({
                    "success": True
                })

        except Exception as e:
            print(f"Error processing attendance: {str(e)}")  # Debugging line
            messages.error(request, "Failed to submit attendance.")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

def logout(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

def apply_leave(request, userid=None):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        }, status=405)

    try:
        try:
            user = User.objects.get(userid=userid)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User not found'
            }, status=404)

        data = json.loads(request.body)

        from_date = data.get('from_date')
        to_date = data.get('to_date')
        half_day = data.get('half_day', 'none')
        reason = data.get('reason')

        if not all([from_date, to_date, reason]):
            messages.error(request, "All fields are required.")
            return JsonResponse({
                'success': False
            }, status=400)

        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()

        if to_date_obj < from_date_obj:
            messages.error(request, "To date cannot be before from date.")
            return JsonResponse({
                'success': False
            }, status=400)

        if from_date_obj < timezone.now().date():
            messages.error(request, "Cannot apply leave for past dates.")
            return JsonResponse({
                'success': False
            }, status=400)

        leave_data = {
            'user': user.username,
            'from_date': from_date,
            'to_date': to_date,
            'half_day': half_day,
            'reason': reason,
            'applied_at': timezone.localtime(timezone.now()).strftime('%H:%M:%S')
        }

        attendance_date = from_date
        current_time = timezone.localtime(timezone.now()).strftime('%H:%M:%S')

        attendance_qs = Attendance.objects.filter(
            attendanceDetails__has_key=attendance_date
        )

        if attendance_qs.exists():
            attendance = attendance_qs.first()
            date_data = attendance.attendanceDetails.get(attendance_date, {})
            attendance_items = date_data.get('AttendanceData', [])

            user_found = False

            for item in attendance_items:
                if item['name'] == user.username:
                    item['status'] = 'leave'
                    item['leave'] = leave_data
                    user_found = True
                    break

            if not user_found:
                attendance_items.append({
                    'name': user.username,
                    'status': 'leave',
                    'submitted_time': current_time,
                    'leave': leave_data
                })

            attendance.attendanceDetails[attendance_date] = {
                'AttendanceData': attendance_items,
                'leave': leave_data
            }

            attendance.save()

        else:
            Attendance.objects.create(
                attendanceDetails={
                    attendance_date: {
                        'AttendanceData': [{
                            'name': user.username,
                            'status': 'leave',
                            'submitted_time': current_time,
                            'leave': leave_data
                        }],
                        'leave': leave_data
                    }
                }
            )

        messages.success(request, "Leave applied successfully.")
        return JsonResponse({
            'success': True
        })

    except json.JSONDecodeError:
        messages.error(request, "Invalid JSON payload.")
        return JsonResponse({
            'success': False
        }, status=400)

    except Exception as e:
        print(f"Error applying leave: {str(e)}")  # Debugging line
        messages.error(request, f"Failed to apply leave: {str(e)}.")
        return JsonResponse({
            'success': False
        }, status=500)

def update_rma_status(request, userid=None):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        }, status=405)

    try:
        data = json.loads(request.body)
        rma_id = data.get('rma_id')
        update_status = data.get('update_status')
        update_date = data.get('update_date')

        rma_record = RMA.objects.get(rmaid=rma_id)
        rma_details = rma_record.rmaDetails
        rma_details['update_status'] = update_status
        rma_details['update_date'] = update_date
        rma_record.rmaDetails = rma_details
        rma_record.save()

        messages.success(request, "RMA status updated successfully.")
        return JsonResponse({
            'success': True
        })

    except RMA.DoesNotExist:
        messages.error(request, "RMA record not found.")
        return JsonResponse({
            'success': False
        }, status=404)

    except Exception as e:
        print(f"Error updating RMA status: {str(e)}")  # Debugging line
        messages.error(request, f"Failed to update RMA status: {str(e)}.")
        return JsonResponse({
            'success': False
        }, status=500)