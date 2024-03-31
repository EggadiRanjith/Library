from django.db import models
from django.utils import timezone

class br(models.Model):
    book_id = models.CharField(max_length=20)  # Add a book_id field
    roll_number = models.CharField(max_length=20)  # Add a roll_number field
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    barrow_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.book_name
