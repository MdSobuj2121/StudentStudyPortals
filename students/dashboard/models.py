from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"
        
        
class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class Semester(models.Model):
    number = models.IntegerField()
    gpa = models.FloatField(default=0.0, editable=False)

    def __str__(self):
        return f"Semester {self.number}"

class Subject(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
    ]

    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    credit_hours = models.IntegerField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name
    

class Syllabus(models.Model):
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='syllabuses/')

    def __str__(self):
        return self.description

class Routine(models.Model):
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='routines/')

    def __str__(self):
        return self.description
    
class StudyMaterial(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='study_materials/')

    def __str__(self):
        return self.name

class ProjectIdea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title