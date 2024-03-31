import os
import sys
import django

# Add the directory containing your Django project to the Python path
sys.path.append(r'C:\Users\Ranjith\OneDrive\Desktop\Django Projects\library')  # Use a raw string literal (r'...')

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')  # Replace 'your_project' with your actual project name

# Initialize Django
django.setup()

# Now you can import and use Django modules
from django.contrib.auth import get_user_model

try:
    User = get_user_model()
    user = User.objects.get(email='ranjitheggadi@gmail.com')  # Replace 'user_email' with the actual email you want to check
    print(user.password)
except User.DoesNotExist:
    print("User not found")
