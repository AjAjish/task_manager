from django.shortcuts import render , redirect
from django.contrib import messages
from .models import User, Task

# Create your views here.

def home(request):
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
    return render(request, 'dashboard.html')

def task(request,userid=None):
    userid = request.session.get('userid')
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

            # Patment data from the form
            price = request.POST.get('price')
            paymentStatus = request.POST.get('paymentStatus')

            # Create a JSON structure for task details
            task_details = {
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
                },
                'payment_info': {
                    'price': price,
                    'paymentStatus': paymentStatus,
                }
            }

            print(f"Task Details JSON: {task_details}")  # Debugging line

            return render(request, 'task.html', {'userid': userid})

    return render(request, 'task.html', {'userid': userid})

def work(request,userid=None):
    return render(request, 'work.html')
