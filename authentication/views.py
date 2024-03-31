from django.shortcuts import render, redirect
from django.contrib.auth import  login , authenticate
from django.contrib.auth.models import User
from django.db import connection
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Student

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Use the custom_authenticate function to check credentials
            user = custom_authenticate(email, password)

            if user is not None:
                
                # Authentication successful, log in the user
                request.session['user_email'] = user.email
                request.session['user_rollnumber'] = user.roll_number
                request.session['user_name'] = user.name
                if user.is_admin==1:
                    request.user = user
                    return redirect('adminindex')
                else:
                    request.user = user
                    return redirect('studentindex')
            else:
                # Authentication failed, display an error message
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})
        except Student.DoesNotExist:
            # Handle the case where the Student with the provided email does not exist
            return render(request, 'login.html', {'error_message': 'User not found'})

    return render(request, 'login.html')
def custom_authenticate(email, password):
    try:
        user = Student.objects.get(email=email)
        if user.password == password:
            return user
        else:
            print("Password does not match")
    except Student.DoesNotExist:
        print("Student not found")
    except Exception as e:
        print("An error occurred:", str(e))

    return None



def forgot_view(request):
    return render(request, 'forgotpassword.html')

# Function to send a password recovery email
def send_password_recovery_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = Student.objects.get(email=email)
            name = Student.name  # Replace with your User model field
            password = Student.password  # Replace with your User model field
        except User.DoesNotExist:
             return render(request, 'forgotpassword.html', {'error_message': 'Email not found in the database.'})

        # Create and send the email
        subject = 'Password Recovery'
        message = f'Hello {name},\n\nYour password recovery details are:\n\n' \
                  f'Name: {name}\nPassword: {password}\n\n' \
                  'Please keep your password safe and do not share it with others.\n\n' \
                  'Best regards,\nYour Sender Name'

        from_email = 'noreplaykitslibrary@gmail.com'  # Replace with your email and name
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return HttpResponse('Recovery email sent! Check your inbox for the password.')
        except Exception as e:
            # Handle email sending error
            return render(request, 'forgotpassword.html', {'error_message': 'Error sending the Email'})

    return render(request, 'login.html')  # Replace 'forgotpassword.html' with your template path