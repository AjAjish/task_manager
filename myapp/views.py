from django.shortcuts import render , redirect
from django.contrib import messages
from django.utils import timezone
from .models import User, Task , Work , SalesAndExpenses , RMA
from django.http import JsonResponse
import json 


today = timezone.now().date().isoformat()

# Create your views here.

def home(request,userid=None):
    userid = request.session.get('userid')
    if userid:
        return render(request, 'base.html', {'userid': userid})
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobileNo = request.POST.get('mobileNo')
        password = (request.POST.get('password'))
        confirmPassword = (request.POST.get('confirmPassword'))  

        # Debugging line to check received data...
        print(
            f"Username: {username}, Email: {email}, MobileNo: {mobileNo}, Password: {password}, ConfirmPassword: {confirmPassword}"
        )

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

        #Debuging line to check received data...
        print(f"Email: {email}, Password: {password}")

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
    userid = request.session.get('userid')
    if userid:
        return render(request, 'dashboard.html', {'userid': userid})
    return render(request, 'dashboard.html')

def task(request,userid=None):
    userid = request.session.get('userid')
    user = User.objects.get(userid=userid) if userid else None
    print(f"UserID from session: {userid}")  # Debugging line
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
                },
                'system_info': {
                    'systemType': systemType,
                    'brand': brand,
                    'model': model,
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

            print(f"Task Details JSON: {task_details}")  # Debugging line

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

        print(f"Assigning work to UserID: {assigned_userid} for TaskID: {work_taskid} with Description: {work_description}")  # Debugging line  

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
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'work.html', {
        'userid': userid,
        'user': users,     # keeping your template variable name
        'tasks': tasks,
        'works': works
    })

def sales_and_expenses_page(request, userid=None):
    
    userid = request.session.get('userid')
    # To shoe only today sales and expenses record
    sales_and_expenses = SalesAndExpenses.objects.filter(salesData__date=today).first()
    print(sales_and_expenses)
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
    print("RMA List:", rma_list)
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
        to_address = request.POST.get('to_address')
        product_name = request.POST.get('product_name')
        serial_number = request.POST.get('serial_number')
        quantity = request.POST.get('quantity')
        sent_date = request.POST.get('sent_date')
        problem_description = request.POST.get('problem_description')

        print(f"RMA Submission - To: {to_address}, Product: {product_name}, Serial: {serial_number}, Quantity: {quantity}, Sent Date: {sent_date}, Problem: {problem_description}")  # Debugging line

        rmaData = {
            'to_address': to_address,
            'product_name': product_name,
            'serial_number': serial_number,
            'quantity': quantity,
            'sent_date': sent_date,
            'problem_description': problem_description
        }

        RMA.objects.create(rmaDetails=rmaData)
        messages.success(request, "RMA request submitted successfully.")
        return redirect('rma', userid=userid)

    return render(request, 'rma.html', {'userid': userid ,"rma_list": rma_list})

def attendance_view(request, userid=None):
    users = User.objects.all()
    userid = request.session.get('userid')
    if not userid:
        return redirect('login')  # or your login page
    return render(request, 'attendance.html', {'userid': userid , 'users': users})

def attendance_submit(request, userid=None):
    userid = request.session.get('userid')
    users = User.objects.all()
    if not userid:
        return redirect('login')  # or your login page
    
    if request.method == 'POST':
        try:

            data = json.loads(request.body)

            attendance_date = list(data.keys())[0]
            attendance_items = data[attendance_date].get('AttendanceData', [])

            print(f"Attendance Date: {attendance_date}, Items: {attendance_items}")  # Debugging line
            messages.success(request, "Attendance submitted successfully.")
            return JsonResponse({
                "success": True,
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