from django.shortcuts import render , redirect
from django.contrib import messages
from .models import User, Task , Work

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

    return render(request, 'work.html', {
        'userid': userid,
        'user': users,     # keeping your template variable name
        'tasks': tasks
    })
