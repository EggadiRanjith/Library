from django.shortcuts import render ,redirect,get_object_or_404
from django.http import Http404
from django.urls import reverse
from students.models import *
from .models import *
from django.core.mail import send_mail
from authentication.models import Student
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import boto3 , os
from django.contrib import messages
from django.utils import timezone
import time
from django.db.models import Q
import pandas as pd



# Create your views here.
def admin_index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Compose and send the email
        try:
            send_mail(
                subject,  # The subject of the email
                f"Name: {name}\nEmail: {email}\nMessage: {message}",  # The content of the email
                email,  # Use the user's email as the sender's email address
                ['ranjitheggadi@gmail.com'],  # Your email address (the recipient)
                fail_silently=False,  # If set to True, errors during email sending will not be suppressed
            )
            messages.success(request, 'Email'' Sent successfully')
            return redirect('adminindex')
        except Exception as e:
            return HttpResponse({'error': 'error', 'error_message': str(e)})  # Return an error JSON response with the exception message
    return render(request,'libraryadmin/adminindex.html')

def register(request):
    return render(request,'libraryadmin/registration.html')

def register_form(request):
    if request.method == 'POST':
        # Access form data from request.POST
        year_select = request.POST.get('yearSelect')
        branch_select = request.POST.get('branchSelect')
        rollno = request.POST.get('rollno')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        # Create an instance of your model and save it
        your_model_instance = Student(
            batch=year_select,
            branch=branch_select,
            roll_number=rollno,
            name=name,
            email=email,
            password=password
        )
        your_model_instance.save()

        # After processing, you can redirect to a success page
        messages.add_message(request, messages.SUCCESS, "Registration successful!", extra_tags='form1')
        return redirect('admin_fetchusersticket')  # Change 'success_page' to your actual success page URL

    return render(request, 'libraryadmin/registration.html')


def registerfile(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']  # Access the uploaded file
        if uploaded_file:
            try:
                # Example: Read a CSV or Excel file into a DataFrame using pandas
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    data = pd.read_excel(uploaded_file, engine='openpyxl')
                else:
                    raise ValueError("Unsupported file format")

                # Process the data as needed
                for index, row in data.iterrows():
                    student = Student(
                        roll_number=row['roll_number'],
                        name=row['name'],
                        email=row['email'],
                        password=row['password'],
                        batch=row['batch'],
                        branch=row['branch']
                    )
                    student.save()

                # Display a success message
                return redirect('admin_fetchusersticket')  # Change 'success_page' to your actual success page URL
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')

    return render(request, 'libraryadmin/registration.html')



def admin_general_books_view(request):
    general_books = GeneralBook.objects.all()
    context = {'GeneralBook': general_books}
    return render(request, 'libraryadmin/generalbooks.html', context)

def admin_journals_books_view(request):
    # Replace 'JournalBook' with your specific model for journals
    journal_books = Journal.objects.all()
    context = {'Journal': journal_books}
    return render(request, 'libraryadmin/journals.html', context)

def admin_novels_books_view(request):
    # Replace 'NovelBook' with your specific model for novels
    novel_books = Novel.objects.all()
    context = {'Novel': novel_books}
    return render(request, 'libraryadmin/novels.html', context)

def admin_papers_books_view(request):
    # Replace 'PaperBook' with your specific model for papers
    paper_books = Paper.objects.all()
    context = {'Paper': paper_books}
    return render(request, 'libraryadmin/papers.html', context)

def admin_render_books(request, template_name, model_name, filter_field=None):
    books = model_name.objects.all()
    
    if filter_field:
        branch = request.GET.get(filter_field)
        if branch:
            books = books.filter(**{filter_field: branch})
    
    context = {model_name.__name__.lower(): books}
    print(context)
    return render(request, f'libraryadmin/{template_name}', context)

def admin_first_year_1_1(request):
    return admin_render_books(request, 'first_year_1_1.html', frst1, filter_field='branch')

def admin_first_year_1_2(request):
    return admin_render_books(request, 'first_year_1_2.html', frst2, filter_field='branch')

def admin_second_year_2_1(request):
    return admin_render_books(request, 'second_year_2_1.html', sc1, filter_field='branch')

def admin_second_year_2_2(request):
    return admin_render_books(request, 'second_year_2_2.html', sc2, filter_field='branch')

def admin_third_year_3_1(request):
    return admin_render_books(request, 'third_year_3_1.html', thr1, filter_field='branch')

def admin_third_year_3_2(request):
    return admin_render_books(request, 'third_year_3_2.html', thr2, filter_field='branch')

def admin_fourth_year_4_1(request):
    return admin_render_books(request, 'fourth_year_4_1.html', fr1, filter_field='branch')


def admin_fourth_year_4_2(request):
    return admin_render_books(request, 'fourth_year_4_2.html', fr2, filter_field='branch')


def update_form_books(request, table, id,next):
    model_class = eval(table)
    updationbooks=model_class.objects.get(id=id)
    context = {'model_class':updationbooks,'model':table}
    return render(request, 'libraryadmin/updationform.html', context)

def updatebookform(request,next):
    if request.method == 'POST':
        table=request.POST.get('table')
        bid=request.POST.get('book_id')
        model=eval(table)
        # Get the book instance based on the provided book_id
        book = get_object_or_404(model, id=bid)
        # Get the new data from the POST request
        new_book_name = request.POST.get('new_book_name')
        new_author = request.POST.get('new_author')
        new_year = request.POST.get('new_year')
        new_genre = request.POST.get('new_genre')

        # Update the book instance with the new data
        book.book_name = new_book_name
        book.book_author = new_author
        book.publish_year = new_year
        book.genre = new_genre

        # Save the updated book instance to the database
        book.save()

        messages.success(request, 'Record updated successfully')

        return redirect(next)  # Redirect to a success page or a different URL


    return render(request, 'libraryadmin/updationform.html', {'book': book})

def delete_course(request, table, id, next):
    try:
        # Get the model class based on the 'table' parameter (assuming 'table' is the model name)
        model_class = eval(table)
    except NameError:
        # Handle the case where 'table' is not a valid model name
        raise Http404("Model not found")

    # Use the model class to retrieve the object to be deleted
    obj = get_object_or_404(model_class, id=id)

    # Delete the object
    obj.delete()

    # Redirect to the specified page (next)
    return redirect(next)


def admin_bookupload(request):
    return render(request,'libraryadmin/uploadbooks.html')

@csrf_exempt
def book_upload_books(request):
    if request.method == "POST":
        category = 'Books'
        subcategory = request.POST.get("category")

        # Determine the appropriate subclass based on the selected category
        if subcategory == "general_books":
            BookModel = GeneralBook
        elif subcategory == "journals":
            BookModel = Journal
        elif subcategory == "papers":
            BookModel = Paper
        elif subcategory == "novels":
            BookModel = Novel
        else:
            return HttpResponse("Invalid category selected")

        # AWS S3 configuration (replace with your AWS credentials)
        aws_access_key_id = 'amazonsecrete'
        aws_secret_access_key = 'amazonsecrete'
        bucket = 'library4'  # Replace with your S3 bucket name
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Handle image upload to Amazon S3
        if request.FILES.get("image"):
            image_file = request.FILES["image"]
            image_s3_key = f"{category}/{subcategory}/images/{image_file.name}"

            s3.upload_fileobj(image_file, bucket, image_s3_key)

        # Handle file upload to Amazon S3
        if request.FILES.get("file"):
            file_file = request.FILES["file"]
            file_s3_key = f"{category}/{subcategory}/files/{file_file.name}"

            s3.upload_fileobj(file_file, bucket, file_s3_key)

        # Store S3 links in your database for retrieval
        image_s3_link = f"https://{bucket}.s3.amazonaws.com/{image_s3_key}"
        file_s3_link = f"https://{bucket}.s3.amazonaws.com/{file_s3_key}"

        # Get form data
        book_name = request.POST.get("bookName")
        book_author = request.POST.get("bookAuthor")
        publish_year = request.POST.get("publishYear")
        genre = request.POST.get("genre")

        # Create a new record in the appropriate subclass
        book_instance = BookModel(
            book_name=book_name,
            image_path=image_s3_link,
            book_author=book_author,
            upload_date="2023-09-04",  # Use the appropriate date format
            genre=genre,
            publish_year=publish_year,
            file_path=file_s3_link,
        )
        book_instance.save()
            # Assign a success message to a variable
        success_message = 'Book uploaded successful!'

        # Set the success message in the messages framework
        messages.success(request, success_message)

        # Render the same view with the success message
        if subcategory == "general_books":
            return redirect('admin_generalbooks')
        elif subcategory == "journals":
            return redirect('admin_journals')
        elif subcategory == "papers":
            return redirect('admin_papers')
        elif subcategory == "novels":
            return redirect('admin_novels')
        else:
            return render(request, 'libraryadmin/uploadbooks.html', {'success_message': success_message})
    else:
        return render(request, 'libraryadmin/uploadbooks.html')  # Render the form page for GET requests

@csrf_exempt
def course_upload(request):
    if request.method == "POST":
        category = 'Courses'
        subcategory = request.POST.get("category")

        # Determine the appropriate course model based on the subcategory
        course_model = None
        if subcategory == 'frst1':
            course_model = frst1
        elif subcategory == 'frst2':
            course_model = frst2
        elif subcategory == 'snd1':
            course_model = sc1
        elif subcategory == 'snd2':
            course_model = sc2
        elif subcategory == 'thr1':
            course_model = thr1
        elif subcategory == 'thr2':
            course_model = thr2
        elif subcategory == 'fr1':
            course_model = fr1
        elif subcategory == 'fr2':
            course_model = fr2

        if course_model is None:
            return HttpResponse("Invalid subcategory selected")

        # AWS S3 configuration
        aws_access_key_id = 'amazonsecrete'
        aws_secret_access_key = 'amazonsecrete'
        bucket_name = 'library4'  # Replace with your S3 bucket name
        image_prefix = f"{category}/{subcategory}/images/"
        file_prefix = f"{category}/{subcategory}/files/"

        # Initialize the S3 client
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Handle image upload to Amazon S3
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            image_file_name = image_file.name
            image_s3_key = os.path.join(image_prefix, image_file_name)

            s3.upload_fileobj(image_file, bucket_name, image_s3_key)

        else:
            # Handle image upload error here
            return HttpResponse("Image upload failed!")

        # Handle file upload to Amazon S3
        if 'file' in request.FILES:
            file_file = request.FILES['file']
            file_file_name = file_file.name
            file_s3_key = os.path.join(file_prefix, file_file_name)

            s3.upload_fileobj(file_file, bucket_name, file_s3_key)

        else:
            # Handle file upload error here
            return HttpResponse("File upload failed!")

        # Store S3 links in your database for retrieval
        image_s3_link = f"https://{bucket_name}.s3.amazonaws.com/{image_s3_key}"
        file_s3_link = f"https://{bucket_name}.s3.amazonaws.com/{file_s3_key}"

        # Get form data
        book_name = request.POST.get("bookName")
        book_author = request.POST.get("bookAuthor")
        publish_year = request.POST.get("publishYear")
        genre = request.POST.get("genre")
        branch = request.POST.get("branchSelect")

        # Create a new record in the appropriate course model
        course_instance = course_model(
            book_name=book_name,
            book_author=book_author,
            publish_year=publish_year,
            genre=genre,
            image_path=image_s3_link,
            file_path=file_s3_link,
            branch=branch,
        )
        course_instance.save()
        success_message = 'Course uploaded successful!'

        # Set the success message in the messages framework
        messages.success(request, success_message)

        # Render the same view with the success message
        if subcategory == 'frst1':
            return redirect('admin_first_year_1_1')
        elif subcategory == 'frst2':
            return redirect('admin_first_year_1_2')
        elif subcategory == 'snd1':
            return redirect('admin_second_year_2_1')
        elif subcategory == 'snd2':
            return redirect('admin_second_year_2_2')
        elif subcategory == 'thr1':
            return redirect('admin_third_year_3_1')
        elif subcategory == 'thr2':
            return redirect('admin_third_year_3_2')
        elif subcategory == 'fr1':
            return redirect('admin_fourth_year_4_1')
        elif subcategory == 'fr2':
           return redirect('admin_fourth_year_4_2')
    else:
        return render(request, 'libraryadmin/uploadboooks.html')  # Render the form page for GET requests
    
@csrf_exempt
def admin_fetch_user_ticket(request):
    return render(request,'libraryadmin/fetchusersticket.html')

@csrf_exempt
def fetchbooks(request):
    if request.method == "POST":
        book_id = request.POST.get("Book_Id")
        data = br.objects.filter(book_id=book_id)  # Use the correct model name here
        context = {'br': data,}
        return render(request, 'libraryadmin/studentsbooks.html', context)
    else:
        return render(request, 'libraryadmin/fetchusersticket.html')  # Render the form page for GET requests
    
@csrf_exempt
def studentbooks(request):
    if request.method == "POST":
        roll_number = request.POST.get("roll_number")
        request.session['fetchroll'] = roll_number
        data = br.objects.filter(roll_number=roll_number) 
        studentdata=Student.objects.get(roll_number=roll_number)# Use the correct model name here
        context = {'br': data, 'Student': studentdata}
        return render(request, 'libraryadmin/studentsbooks.html', context)
    else:
        return render(request, 'libraryadmin/fetchusersticket.html')  # Render the form page for GET requests
    

@csrf_exempt
def borrow_return(request):
    fetchedroll= request.session.get('fetchroll')
    on_loan = "on Loan"
    rbook = br.objects.filter(roll_number=fetchedroll, status=on_loan)
    context = {
        'fetchedroll': fetchedroll,
        'rbook': rbook,
    }
    return render(request,'libraryadmin/br.html',context)

@csrf_exempt
def borrow_book(request):
    if request.method == "POST":
        roll_number = request.POST.get("roll_number")
        book_id = request.POST.get("bookid")
        book_name = request.POST.get("bookName")
        book_author = request.POST.get("bookAuthor")
        on_loan = "on Loan"
        borrow_date = timezone.now().strftime('%Y-%m-%d %H:%M:%S.%f%z')  # Replace with the actual date

        try:
            # Get the user from the database
            user = Student.objects.get(roll_number=roll_number)

            # Check if the user has available tickets (ticket_count > 0)
            if user.tickets > 0:
                # Update the user's ticket count
                user.tickets -= 1
                user.save()

                # Create a new record for the borrowed book
                borrowed_book = br(
                    roll_number=roll_number,
                    book_id=book_id,
                    book_name=book_name,
                    author=book_author,
                    status=on_loan,
                    barrow_date=borrow_date,
                )
                borrowed_book.save()

                # Send an email to the user
                send_mail(
                    'Book Borrowing Request Confirmation',
                    f'Hello {user.name},\n\n'
                    f'Thank you for borrowing a book from our library. Here are the details of your borrowing:\n\n'
                    f'Book Id: {book_id}\n'
                    f'Book Title: {book_name}\n'
                    f'Borrow Date: {borrow_date}\n'
                    f'Please ensure to return the book on or before the specified return date to avoid any late fees.\n\n'
                    f'Happy reading!\n\n'
                    f'Best regards,\n'
                    f'Your Library Team',
                    'noreply@kitslibrary.com',  # Replace with your email address
                    [user.email],  # Replace with the user's email address
                    fail_silently=False,
                )
                
                messages.success(request, 'Record updated successfully and Redirecting to Tickets','borrow')
                   # Suppose you want to go back to a view named 'previous_view'
                return redirect('studentbooks')
            else:
                return HttpResponse("Tickets are not sufficient, please return any book!")
        except Student.DoesNotExist:
            return HttpResponse("User not found!")

    return render(request,' br.html')  # Render the form page for GET requests
@csrf_exempt
def return_book(request):
    if request.method == "POST":
        roll_number = request.POST.get("roll_number")
        book_id = request.POST.get("book_id")
        on_loan = "Returned"
        returned = timezone.now()

        try:
            # Update the database record for the returned book
            book = br.objects.get(roll_number=roll_number, book_id=book_id)
            book.status = on_loan
            book.return_date= returned
            book.save()

            # Fetch user details
            user_details = Student.objects.get(roll_number=roll_number)
            user_details.tickets +=1
            user_details.save()

            # Send confirmation email
            subject = "Book Return Confirmation"
            message = (
                f"Hello {user_details.name},\n\n"
                f"Thank you for returning the book to our library.\n\n"
                f"Here are the details of your book return:\n"
                f"Book Id: {book_id}\n"
                f"Returned Date: {returned}\n\n"
                f"We appreciate your cooperation in returning the book on time.\n\n"
                f"If you have any other books borrowed from us, please ensure to return them according to the specified return dates.\n\n"
                f"Happy reading!\n\n"
                f"Best regards,\n"
                f"Your Library Team"
            )

            send_mail(
                subject, message, "noreply@kitslibrary.com", [user_details.email]
            )

            messages.success(request, 'Book returned successfully! and Redirecting to Tickets')
                   # Suppose you want to go back to a view named 'previous_view'
            return redirect('studentbooks')
        
        except Exception as e:
            print(e)
            messages.error(request, "Error in Returning!")

    return redirect("br")
    
def admin_profile(request):
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
    return render(request, 'libraryadmin/profile.html', context)

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
            
    return render(request,'libraryadmin/profile.html')

def logout(request):
    # Delete the user's session
    request.session.flush()
    # Redirect to a specific URL (e.g., the home page)
    return redirect('login')