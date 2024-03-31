from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Student(models.Model):
    roll_number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    batch = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    
    # Add the tickets field
    tickets = models.PositiveIntegerField(
        default=4,
        validators=[
            MaxValueValidator(4, message=""),
            MinValueValidator(0, message=""),
        ],
    )
    is_admin = models.IntegerField(
        default=0,
        choices=[
            (0, 'No'),  # 0 represents 'No'
            (1, 'Yes'),  # 1 represents 'Yes'
        ],

    )