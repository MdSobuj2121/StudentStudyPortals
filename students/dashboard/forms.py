from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields=['title', 'description']
        
class DateInput(forms.DateInput):
    input_type = 'date'
    
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
        
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter your topics: ")
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']
        
class ConversionForm(forms.Form):
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
class ConversionLengthForm(forms.Form):
    CHOICES = [('yard', 'Yard'), ('foot', 'Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type': 'number', 'placeholder': 'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label='',widget = forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label='',widget = forms.Select(choices = CHOICES)
    )
    
class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type': 'number', 'placeholder': 'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label='',widget = forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label='',widget = forms.Select(choices = CHOICES)
    )
    
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'credit_hours', 'semester']

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['number']
        
        
class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['description', 'file']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['description', 'file']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        
class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['name', 'file']

class ProjectIdeaForm(forms.ModelForm):
    class Meta:
        model = ProjectIdea
        fields = ['title', 'description']