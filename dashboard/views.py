from django.shortcuts import render, redirect
from .models import Notes, Homework, Todo,HomeModel
from .forms import *
from django.contrib import messages
from django.views.generic.detail import DetailView
from youtubesearchpython import VideosSearch
import requests
import json
import wikipedia
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from PyDictionary import PyDictionary
from django.contrib.auth import logout
# Create your views here.
def Home(request):
    homes = HomeModel.objects.all()
    return render(request, 'dashboard/home.html',{'homes':homes})

@login_required
def StudentNotes(request):
    if request.method == 'POST':
        forms = NotesForm(request.POST)
        if forms.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            forms = NotesForm()
        messages.success(request,f"Notes Added from {request.user.username} Successfully")

    else:
        forms = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    return render(request, 'dashboard/notes.html',{'notes':notes,'forms':forms})

@login_required
def DeleteNotes(request, pk=None):
    Notes.objects.get(id=pk).delete()
    messages.success(request,f"Notes Deleted from {request.user.username} Successfully")
    return redirect('/notes/')


class NotesDetailView(DetailView):
    model = Notes

@login_required
def HomeWork(request):
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
                user=request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request, f"Homework Added from {request.user.username}!!")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    


    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    return render(request, 'dashboard/homework.html',{'homeworks':homework,'homework_done': homework_done,'form':form})

@login_required
def Update_Homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
        
    else:
        homework.is_finished = True
    
    homework.save()
    return redirect('homework page')

@login_required
def Delete_Homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework page')

def Youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnails' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i ['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)

        return render(request, 'dashboard/youtube.html',{'form':form, 'results':result_list})
    else:
        form = DashboardForm()
    return render(request, 'dashboard/youtube.html',{'form':form})


@login_required
def TodoList(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
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
            messages.success(request, f"Todo Added from {request.user.username} ")
            todos.save()
    
    else:        
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    return render(request,'dashboard/todo.html',{'todos':todo, 'form':form, 'todos_done':todos_done})


@login_required
def Update_todo(request, pk):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False

    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo page')

@login_required
def Delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo page')


def Books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                'subtitle' : answer['items'][i]['volumeInfo'].get('subtitle'),
                'description' : answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories' : answer['items'][i]['volumeInfo'].get('categories'),
                'rating' : answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail' : answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview' : answer['items'][i]['volumeInfo'].get('previewLink'),
            }
        
            result_list.append(result_dict)
        


        return render(request, 'dashboard/books.html',{'form':form, 'results':result_list})
    else:
        form = DashboardForm()
    return render(request, 'dashboard/books.html',{'form':form})


def Dictionary(request):

    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        dictionary = PyDictionary()
        meanings = dictionary.meaning(text)
 
        # getting a synonym and antonym  
        # synonyms = dictionary.synonym(text)
        # antonyms = dictionary.antonym(text)
        # bundling all the variables in the context  
        context = {
                'form' : form,
                'input': text,
                'meanings':meanings,
                # 'synonyms':synonyms,
                # 'phonetics':antonyms
            }
        # url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        # r = requests.get(url)
        # answer = r.json()
        # try:
        #     phonetics = answer[0]['phonetics'][0]['text']
        #     audio = answer[0]['phonetics'][0]['audio']
        #     definition = answer[0]['meanings'][0]['definitions'][0]['definition']
        #     example = answer[0]['meanings'][0]['definitions'][0]['example']
        #     synonyms = answer[0]['meanings'][0]['definition'][0]['synonyms']
        #     context = {
        #             'form' : form,
        #             'input' : text,
        #             'phonetics' : phonetics,
        #             'audio' : audio,
        #             'definition' : definition,
        #             'example' : example,
        #             'synonyms' : synonyms,
        #         }
        # except:
        #     context = {
        #             'form' : form,
        #             'input' : '',}
   
        return render(request,'dashboard/dictionary.html', context)
    
    else:        
        form = DashboardForm()
      
    return render(request,'dashboard/dictionary.html',{ 'form' : form,})


def Wiki(request):
    
    if request.method == 'POST':
        try:
            text = request.POST['text']
            form = DashboardForm(request.POST)
            search = wikipedia.page(text)
            context ={
                'form':form,
                'title':search.title,
                'link':search.url,
                'details':search.summary
            }
        except:
            context ={
                'form':form,}
        return render(request,'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
    return render(request,'dashboard/wiki.html',{'form' : form})


def Conversion(request):
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
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                    context = {
                        'form' : form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer,
                    }
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
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                    context = {
                        'form' : form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer,
                            }
   
    else:          
        form = ConversionForm()
        context = {
            'form' : form,
            'input' : False
        }
    return render(request,'dashboard/conversion.html', context)


def Register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request,'dashboard/register.html',{'form':form})
 

@login_required
def Profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    
    context = {
        'homeworks' :homeworks,
        'todos' : todos,
        'homework_done' : homework_done,
        'todo_done' : todo_done,
    }
    return render(request,'dashboard/profile.html', context)


def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Successfull")
    return redirect("/login/")