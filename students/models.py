from django.db import models

# Abstract base class for books
class Book(models.Model):
    book_name = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    upload_date = models.DateField()
    genre = models.CharField(max_length=50)
    publish_year = models.PositiveIntegerField()
    file_path = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.book_name

# Create models for specific book types inheriting from the abstract base class
class GeneralBook(Book):
    pass

class Journal(Book):
    pass

class Paper(Book):
    pass

class Novel(Book):
    pass

class courses(models.Model):
    book_name = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    book_author = models.CharField(max_length=100)
    publish_year = models.IntegerField(null=True, blank=True)
    file_path = models.CharField(max_length=255)
    branch = models.CharField(max_length=50, null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
      abstract = True
        
    def __str__(self):
        return self.book_name

class frst1(courses):
    pass

class frst2(courses):
    pass

class sc1(courses):
    pass

class sc2(courses):
    pass

class thr1(courses):
    pass

class thr2(courses):
    pass

class fr1(courses):
    pass

class fr2(courses):
    pass