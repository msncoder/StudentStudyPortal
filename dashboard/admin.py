from django.contrib import admin
from .models import Notes,Homework, Todo, HomeModel
# Register your models here.

@admin.register(HomeModel)
class HomeAdmin(admin.ModelAdmin):
    list_display = ['id','url','images','title','desc']

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','description']


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id','user','title' ,'is_finished']


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['id','user','subject','title','description','due','is_finished']