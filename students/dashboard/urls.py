from django.urls import path
from . import views
from .views import NotesDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('notes', views.notes, name="notes"),
    path('delete_note/<int:pk>', views.delete_note, name="delete-note"),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name="notes-detail"),
    path('homework', views.homework, name="homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete-homework"),
    path('youtube', views.youtube, name="youtube"),
    path('todo', views.todo, name="todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete-todo"),
    path('books', views.books, name="books"),
    path('dictionary', views.dictionary, name="dictionary"),
    path('wiki', views.wiki, name="wiki"),
    path('conversion', views.conversion, name="conversion"),
    path('chat', views.chat, name="chat"),
    path('cgpa', views.cgpa_view, name='cgpa_view'),
    path('syllabus_routine_view', views.syllabus_routine_view, name='syllabus_routine_view'),
    path('syllabus/add/', views.SyllabusCreateView.as_view(), name='add_syllabus'),
    path('routine/add/', views.RoutineCreateView.as_view(), name='add_routine'),
    path('delete_syllabus/<int:pk>/', views.SyllabusDeleteView.as_view(), name='delete_syllabus'),
    path('delete_routine/<int:pk>/', views.RoutineDeleteView.as_view(), name='delete_routine'),
    path('whiteboard/', views.whiteboard_view, name='whiteboard'),
    path('study_materials/', views.study_materials_list, name='study_materials_list'),
    path('study_materials/add/', views.add_study_material, name='add_study_material'),
    path('study_materials/<int:pk>/delete/', views.delete_study_material, name='delete_study_material'),
    path('project_ideas/', views.project_ideas_list, name='project_ideas_list'),
    path('project_ideas/add/', views.add_project_idea, name='add_project_idea'),
    path('project_ideas/<int:pk>/delete/', views.delete_project_idea, name='delete_project_idea'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)