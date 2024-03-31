from django.shortcuts import render,redirect
from .models import *
from libraryadmin.models import *
from authentication.models import Student
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse


# Create your views here.
def student_index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Compose and send the email
        try:
            print('hi')
            send_mail(
                subject,  # The subject of the email
                f"Name: {name}\nEmail: {email}\nMessage: {message}",  # The content of the email
                email,  # Use the user's email as the sender's email address
                ['ranjitheggadi@gmail.com'],  # Your email address (the recipient)
                fail_silently=False,  # If set to True, errors during email sending will not be suppressed
            )
            messages.success(request, 'Email Sent successfully')
            return redirect('studentindex')
        except Exception as e:
            return HttpResponse({'error': 'error', 'error_message': str(e)})  # Return an error JSON response with the exception message

    return render(request, 'studentindex.html')


def general_books_view(request):
    general_books = GeneralBook.objects.all()
    context = {'GeneralBook': general_books}
    return render(request, 'generalbooks.html', context)

def journals_books_view(request):
    # Replace 'JournalBook' with your specific model for journals
    journal_books = Journal.objects.all()
    context = {'Journal': journal_books}
    return render(request, 'journals.html', context)

def novels_books_view(request):
    # Replace 'NovelBook' with your specific model for novels
    novel_books = Novel.objects.all()
    context = {'Novel': novel_books}
    return render(request, 'novels.html', context)

def papers_books_view(request):
    # Replace 'PaperBook' with your specific model for papers
    paper_books = Paper.objects.all()
    context = {'Paper': paper_books}
    return render(request, 'papers.html', context)

def render_books(request, template_name, model_name, filter_field=None):
    if filter_field:
        books = model_name.objects.filter(**{filter_field: request.GET.get(filter_field)})
    else:
        books = model_name.objects.all()
    context = {model_name.__name__.lower(): books}
    return render(request, template_name, context)

def first_year_1_1(request):
    return render_books(request, 'first_year_1_1.html', frst1, filter_field='branch')

def first_year_1_2(request):
    return render_books(request, 'first_year_1_2.html', frst2)

def second_year_2_1(request):
    return render_books(request, 'second_year_2_1.html', sc1)

def second_year_2_2(request):
    return render_books(request, 'second_year_2_2.html', sc2)

def third_year_3_1(request):
    return render_books(request, 'third_year_3_1.html', thr1)

def fourth_year_4_1(request):
    return render_books(request, 'fourth_year_4_1.html', thr2)

def third_year_3_2(request):
    return render_books(request, 'third_year_3_2.html', fr1)

def fourth_year_4_2(request):
    return render_books(request, 'fourth_year_4_2.html', fr2)

def fetch_user_ticket(request):
    roll_number = request.session.get('user_rollnumber')
    data = br.objects.filter(roll_number=roll_number) 
    studentdata= Student.objects.get(roll_number=roll_number)
    context = {'br': data,'Student':studentdata}
    return render(request,'fetchusersticket.html',context)

def studentprofile(request):
    user_email = request.session.get('user_email')
    user_rollnumber = request.session.get('user_rollnumber')
    user_name = request.session.get('user_name')

    # Create a context dictionary with the user-related information
    context = {
        'user_email': user_email,
        'user_rollnumber': user_rollnumber,
        'user_name': user_name,
    }

    # Render the template with the context data
    return render(request, 'profile.html', context)

def change_password(request):
    user_email = request.session.get('user_email')
    if request.method == 'POST':
        oldpassword = request.POST['old_password']
        newpassword = request.POST['new_password']
        confirmpassword = request.POST['confirm_password']
        
        # Retrieve the user based on their email
        user = Student.objects.get(email=user_email)

        # Check if the old password matches the user's current password
        if user.password==oldpassword:

            # Update the user's password field with the new hashed password
            user.password = newpassword
            user.save()

            messages.success(request, 'Password changed successfully.')
            return redirect('profile')  # Redirect to the user's profile page
        else:
            messages.error(request, 'Old password is incorrect.')
            
    return render(request,'profile.html')

def logout(request):
    # Delete the user's session
    request.session.flush()
    # Redirect to a specific URL (e.g., the home page)
    return redirect('login')