from django.shortcuts import redirect, render, get_object_or_404
from . forms import *
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from youtubesearchpython import VideosSearch
from django.views.generic import DeleteView
from .models import Subject, Semester
from .forms import SubjectForm, SemesterForm
import requests
from django.views.generic import CreateView
import wikipedia
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request, f"Notes Added from {request.user.username} Successfully")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user = request.user)
    context={
        'form': form,
        'notes': notes,
    }
    return render(request, 'dashboard/notes.html', context)
@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes

@login_required  
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request, f"Homework Added from {request.user.username} Successfully")
    else:        
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homework_done': homework_done,
        'homeworks': homework,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")
@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")
@login_required
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        videos = VideosSearch(text, limit=20)
        result_list = []
        for i in videos.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list,
            }
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/youtube.html', context)
@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request, f"Todo Added from {request.user.username} Successfully")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user = request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'todos': todo,
        'form': form,
        'todo_done': todo_done
    }
    return render(request, 'dashboard/todo.html', context)
@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect("todo")
@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

@login_required
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q=' + text
        r = requests.get(url)
        ans = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': ans['items'][i]['volumeInfo']['title'],
                'subtitle': ans['items'][i]['volumeInfo'].get('subtitle'),
                'description': ans['items'][i]['volumeInfo'].get('description'),
                'count': ans['items'][i]['volumeInfo'].get('pageCount'),
                'categories': ans['items'][i]['volumeInfo'].get('categories'),
                'rating': ans['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': ans['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': ans['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
        context = {
            'form': form,
            'results': result_list,
        }
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/books.html', context)

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + text
        r = requests.get(url)
        ans = r.json()
        try:
            phonetics = ans[0]['phonetics'][0]['text']
            audio = ans[0]['phonetics'][0]['audio']
            definition = ans[0]['meanings'][0]['definitions'][0]['definition']
            example = ans[0]['meanings'][0]['definitions'][0]['example']
            synonyms = ans[0]['meanings'][0]['definitions'][0]['synonyms']
            context={
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
            }
        except:
            context={
                'form': form,
                'input': '',
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form,
        }
    return render(request, 'dashboard/dictionary.html', context)

@login_required
def wiki(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        search = wikipedia.page(text)
        context={
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary,
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context={
            'form': form
        }
    return render(request, 'dashboard/wiki.html', context)

def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} Yard = {int(input)*3} Foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} Foot = {int(input)/3} Yard'
                context = {
                'form':form,
                'm_form':measurement_form,
                'input':True,
                'answer':answer
            }
        else:
          if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} Pound = {int(input)*0.453592} Kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} Kilogram = {int(input)*2.20462} Pound'
                context = {
                'form':form,
                'm_form':measurement_form,
                'input':True,
                'answer':answer
            }    

    else:
        form = ConversionForm()
        context = {
            'form':form,
            'input':False
        }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username}!!")
            redirect("login")
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request,"dashboard/register.html",context)
@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True 
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True 
    else:
        todos_done = False
    context = {
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }
    return render(request,'dashboard/profile.html', context)


def chat(request):
    return render(request, 'dashboard/chat.html')

def calculate_gpa(subjects):
    grade_points = {
        'A+': 4.0,
        'A': 3.75,
        'A-': 3.5,
        'B+': 3.25,
        'B': 3.0,
        'B-': 2.75,
        'C+': 2.5,
        'C': 2.25,
        'D': 2.0,
        'F': 0.0,
    }
    
    total_points = 0
    total_credits = 0
    for subject in subjects:
        grade = subject.grade
        total_points += grade_points[grade] * subject.credit_hours
        total_credits += subject.credit_hours
    
    return total_points / total_credits if total_credits > 0 else 0
@login_required
def cgpa_view(request):
    semesters = Semester.objects.all()
    all_subjects = Subject.objects.all()
    cgpa = 0
    total_gpa = 0
    total_semesters = len(semesters)

    if request.method == 'POST':
        if 'add_semester' in request.POST:
            semester_form = SemesterForm(request.POST)
            if semester_form.is_valid():
                semester = semester_form.save()
                subjects = Subject.objects.filter(semester=semester)
                gpa = calculate_gpa(subjects)
                semester.gpa = gpa
                semester.save()
                return redirect('cgpa_view')
        elif 'add_subject' in request.POST:
            subject_form = SubjectForm(request.POST)
            if subject_form.is_valid():
                subject_form.save()
                return redirect('cgpa_view')
        elif 'reset_data' in request.POST:
            Semester.objects.all().delete()
            Subject.objects.all().delete()
            return redirect('cgpa_view')
    else:
        semester_form = SemesterForm()
        subject_form = SubjectForm()
    
    for semester in semesters:
        subjects = Subject.objects.filter(semester=semester)
        semester.gpa = calculate_gpa(subjects)
        total_gpa += semester.gpa
    
    cgpa = total_gpa / total_semesters if total_semesters > 0 else 0

    context = {
        'semesters': semesters,
        'cgpa': cgpa,
        'semester_form': semester_form,
        'subject_form': subject_form,
        'all_subjects': all_subjects,
    }

    return render(request, 'dashboard/cgpa.html', context)
@login_required
def syllabus_routine_view(request):
    syllabuses = Syllabus.objects.all()
    routines = Routine.objects.all()
    syllabus_form = SyllabusForm()
    routine_form = RoutineForm()

    if request.method == 'POST':
        if 'syllabus' in request.POST:
            syllabus_form = SyllabusForm(request.POST, request.FILES)
            if syllabus_form.is_valid():
                syllabus_form.save()
                return redirect('syllabus_routine_view')
        elif 'routine' in request.POST:
            routine_form = RoutineForm(request.POST, request.FILES)
            if routine_form.is_valid():
                routine_form.save()
                return redirect('syllabus_routine_view')

    context = {
        'syllabuses': syllabuses,
        'routines': routines,
        'syllabus_form': syllabus_form,
        'routine_form': routine_form,
    }

    return render(request, 'dashboard/syllabus_routine.html', context)

class SyllabusCreateView(CreateView):
    model = Syllabus
    form_class = SyllabusForm
    template_name = 'dashboard/syllabus_form.html'
    success_url = reverse_lazy('syllabus_routine_view')

class RoutineCreateView(CreateView):
    model = Routine
    form_class = RoutineForm
    template_name = 'dashboard/routine_form.html'
    success_url = reverse_lazy('syllabus_routine_view')
    
class SyllabusDeleteView(DeleteView):
    model = Syllabus
    success_url = reverse_lazy('syllabus_routine_view')
    template_name = 'dashboard/syllabus_confirm_delete.html'

class RoutineDeleteView(DeleteView):
    model = Routine
    success_url = reverse_lazy('syllabus_routine_view')
    template_name = 'dashboard/routine_confirm_delete.html'
    
def whiteboard_view(request):
    return render(request, 'dashboard/whiteboard.html')

@login_required
def study_materials_list(request):
    study_materials = StudyMaterial.objects.all()
    return render(request, 'dashboard/study_materials_list.html', {'study_materials': study_materials})

def add_study_material(request):
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('study_materials_list')
    else:
        form = StudyMaterialForm()
    return render(request, 'dashboard/add_study_material.html', {'form': form})

def delete_study_material(request, pk):
    study_material = get_object_or_404(StudyMaterial, pk=pk)
    if request.method == 'POST':
        study_material.delete()
        return redirect('study_materials_list')
    return render(request, 'dashboard/delete_study_material.html', {'study_material': study_material})
@login_required
def project_ideas_list(request):
    project_ideas = ProjectIdea.objects.all()
    return render(request, 'dashboard/project_ideas_list.html', {'project_ideas': project_ideas})

def add_project_idea(request):
    if request.method == 'POST':
        form = ProjectIdeaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_ideas_list')
    else:
        form = ProjectIdeaForm()
    return render(request, 'dashboard/add_project_idea.html', {'form': form})

def delete_project_idea(request, pk):
    project_idea = get_object_or_404(ProjectIdea, pk=pk)
    if request.method == 'POST':
        project_idea.delete()
        return redirect('project_ideas_list')
    return render(request, 'dashboard/delete_project_idea.html', {'project_idea': project_idea})