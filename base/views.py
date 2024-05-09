from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import  Q
from icecream import ic
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# rooms=[
#     {'id':1,'name':'learn python!'},
#     {'id':2,'name':'Design with me !'},
#     {'id':3,'name':'Frontend developers !'}

# ]
def loginPage(request):# learn about request parameter  https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139
    page='login'
    if request.user.is_authenticated:  # if user is login in already then user if you give url http://127.0.0.1:8000/login and click enter then it is directly go to home page 
        return redirect('home')
    if request.method == 'POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')
        try:
            username=User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")
        user=authenticate(request,email=email,password=password)   
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "username or passoword does not exist")
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):# learn about request parameter  https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139
    logout(request)   # delete the csrf token if user is logged out 
    return redirect('home')

def registerPage(request):
    page='register'
    form=MyUserCreationForm()
    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False) # because if user enter the Captial alpabet neec to convert intolover case we are pausing the save means holding
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"error occured during registration")
    context={'page':page,'form':form}

    return  render(request,'base/login_register.html',context)


 # if user is logiout 
def home(request):# learn about request parameter  https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139
    q=request.GET.get('q') if request.GET.get('q')!=None else '' ## table  need to understand the how if condition is fixed
    
    ic(q)
    rooms=Room.objects.filter(Q(topic__name__icontains=q)|Q(description__icontains=q)|Q(name__icontains=q))   # topic__name__icontains means topic contain name soo we are using tapic__name then icontains is means contain data 
    rooms_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))   # toom_>topoic->name
    ic(rooms)
    topics=Topic.objects.all()[0:5]
    ic(rooms)
    context={'rooms':rooms,'topics':topics,'rooms_count':rooms_count,'room_messages':room_messages}
    ic(context)
    return render(request,'base/home.html',context)


def room(request,pk):# learn about request parameter  https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139
    room =None
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()  # many to one relationship there so that we are using message_set.all()

    participants=room.participants.all()

    if request.method == 'POST':
        message=Message.objects.create(user=request.user,room=room,body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,'room_messages':room_messages,'participants':participants}
   

    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    room_messages=user.message_set.all()
    context={'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages}
   
    
    return render(request,'base/profile.html',context)
@login_required(login_url='login')   # login user can create room 
def createRoom(request):# learn about request parameter  https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139
    ic(1)
    form = RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
       topic_name = request.POST.get('topic')
       topic,created=Topic.objects.get_or_create(name=topic_name)
       Room.objects.create(
           host=request.user,
           topic=topic,
           name=request.POST.get('name'),
           description=request.POST.get('description')
           
       )
       return redirect('home')
    #    form = RoomForm(request.POST)

    #    if form.is_valid():
           
    #        form.save(commit=False)
    #        room.host=request.user
    #        room.save()
        
    
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login') # login user can update room 
def updateRoom(request,pk):   # learn about request parameter  https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139
    ic(request)
    room = Room.objects.get(id=pk)
    topics=Topic.objects.all()
    form =RoomForm(instance=room) # already selected data to show that purpose using 
    if request.user!=room.host:
        return HttpResponse("Your not allowed to change ")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form,"topics":topics,'room':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')  # login user can delete room 
def deleteRoom(request,pk):# learn about request parameter  https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139
    room = Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse("Your not allowed to change ")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})



@login_required(login_url='login')  # login user can delete room 
def deleteMessage(request,pk):# learn about request parameter  https://medium.com/@ashishkush1122/understanding-request-object-in-in-django-39c4eb5c3139
    message = Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse("Your not allowed to change ")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method == 'POST':
        form =UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request,'base/update-user.html',{'form':form})

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else '' ## table  need to understand the how if condition is fixed
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})


def activityPage(request):
    room_messages=Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})
