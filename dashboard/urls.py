from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home, name='home page'),
    path('youtube/', views.Youtube, name='youtube page'),
    path('todo/', views.TodoList, name='todo page'),
    path('books/', views.Books, name='books page'),
    path('wiki/', views.Wiki, name='wiki page'),
    path('conversion/', views.Conversion, name='conversion page'),
    path('dictionary/', views.Dictionary, name='dictionary page'),
    path('notes/', views.StudentNotes, name='notes page'),
    path('delete_notes/<int:pk>', views.DeleteNotes, name='delete notes page'),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name='notes detail page'),
    path('homework/', views.HomeWork, name='homework page'),
    path('update_homework/<int:pk>/', views.Update_Homework, name='update homework page'),
    path('update_todo/<int:pk>/', views.Update_todo, name='update todo page'),
    path('delete_todo/<int:pk>/', views.Delete_todo, name='delete todo page'),
    path('delete_homework/<int:pk>/', views.Delete_Homework, name='delete homework page'),

]
