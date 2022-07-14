from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.forms import RoomForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from base.models import Room, Topic, Message


# rooms = [
#     {'id':1, 'name':'learn python'},
#     {'id':2, 'name':'learn Oop'},
#     {'id':3, 'name':'learn html and css'},
#     {'id':4, 'name':'learn sql'},
    
# ]


def loginPage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)

        except:
            messages.error(request, 'User Doesnot Exits')

        user = authenticate(request, username = username, password= password)

        if user is not None:
            login(request, user)
            return redirect('/')
    context={'page':page}
    return render(request,'login_registration.html', context)    

def logoutUser(request):
    logout(request) #delete the session key 
    return redirect('/')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
         user = form.save(commit=False) #hold after the post 
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('/')
        else:
         messages.error(request, 'error in registration')
    context={'form':form}
    return render(request, 'login_registration.html', context)
    


def home(request):
   q = request.GET.get('q') if request.GET.get('q') != None else '' 
   rooms = Room.objects.filter(Q(topic__name__icontains=q)|
   Q(name__icontains =q)|
   Q(discription__icontains =q)|
   Q(host__username =q)|
   Q(host__first_name=q)|
   Q(created__icontains =q)   #linear search algorithm 
   ) #query upward method
   room_count = rooms.count()
   topics = Topic.objects.all()[0:5]
   room_message = Message.objects.filter(Q(room__topic__name__icontains =q))[0:7]
   context ={'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_message':room_message}
   return render(request, 'home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk) #get a single object where the filter is to get the multiple
    # room = None
    # for x in rooms:
    #     if x['id'] == int(pk):
    #      room = x 
    room_messages = room.message_set.all() #give all the message related to the room
    participants = room.participants.all() #many to many relationship
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk =room.id) #fully reloades the room

    context={'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'room.html', context)

def userProfile(request , pk):
    user =User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all() 
    topics = Topic.objects.all()
    context={'user':user, 'rooms':rooms,'room_message':room_message,'topics':topics}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics =Topic.objects.all()
    if request.method =="POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name= topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            discription  = request.POST.get('discription')
        )
        # form = RoomForm(request.POST)
        # print(request.POST)
        # if form.is_valid():
        #  room =form.save( commit=False)
        #  room.host = request.user
        #  room.save()
        return redirect('home')
    context ={'form':form,'topics':topics}
    return render(request, 'room_form.html', context)    

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #prefilled data in the form
    topics =Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Sorry you are not allowed')
    if request.method =='POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name= topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.discription = request.POST.get('discription')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}
    return render(request,'room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("Sorry You cant Delete the room")
    if request.method =="POST":
        room.delete()
        return redirect('home')
    return render(request,'delete.html')

@login_required(login_url='login')
def deleteMessage(request, pk):
    message= Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("you cant dlt this message")

    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':message})        
    
@login_required(login_url='login')
def updateUser(request):
    user =request.user
    form = UserForm(instance= user)

    if request.method =="POST":
        form = UserForm(request.POST, instance =user)
        if form.is_valid():
            form.save()
        return redirect('user-profile',pk =user.id )    
    return render(request,'update-user.html', {'form':form})    


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    topics = Topic.objects.filter(name__icontains =q)
    return render(request, 'topics.html', {'topics':topics})    


def activityPage(request):
    room_messages = Message.objects.all 
    return render(request, 'activity.html' ,{'room_messages':room_messages})
