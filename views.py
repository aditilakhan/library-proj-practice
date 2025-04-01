from django.shortcuts import render, HttpResponse, redirect
from .models import Book
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout


# def index(req):
#     allBooks= Book.objects.all()
#     print(allBooks)
#     return HttpResponse(f"All Books:{allBooks}")

from datetime import datetime

def index(req):
    allBooks= Book.objects.all()
    print(allBooks)
    # context = {"myname": "ITV"}
    # return render(req, 'index.html', context)
    
    myname = "ITV"
    print(datetime.now())
    curdate = datetime.now()
    hour = datetime.now().hour
    print(hour)
    context = {"myname": myname, "curdate": curdate, "hour": hour, "allBooks": allBooks}
    return render(req, "index.html", context)


def signup(req):
    
    if req.method=="GET":
        print(req.method)
        return render(req, "signup.html")
    else:
        print(req.method)
        uname = req.POST["uname"]
        uemail = req.POST["uemail"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        print(uname, upass, ucpass, uemail)
        if upass!=ucpass:
            errmsg='Password and confirm password must be same'
            context={'errmsg':errmsg}
            return render(req, 'signup.html', context)
        elif uname==upass:
            errmsg = "Password should not be same as email id"
            context = {"errmsg": errmsg}
            return render(req, 'signup.html', context)
        else:
            try:
                userdata = User.objects.create(username=uname, email=uemail, password=upass)
                userdata.set_password(upass)
                userdata.save()
                print(User.objects.all())
                return redirect("signin")   
            except:
                errmsg = "User already exists. try with different username"
                context = {"errmsg": errmsg}
                return render(req, 'signup.html', context)
            

def signin(req):
    if req.method=="GET":
        print(req.method)
        return render(req, "signin.html")
    else:
        uname = req.POST.get("uname")
        uemail=req.POST.get("uemail")
        upass=req.POST.get("upass")
        print(uname, uemail,upass)
        # userdata = User.objects.filter(email=uemail,password=upass)
        userdata=authenticate(username=uname, email=uemail,password=upass)
        print(userdata)
        if userdata is not None:
           login(req, userdata)
           return render(req, "dashboard.html")
        else:
            context={}
            context['errmsg']="Invalid email or password"
            return render(req, "signin.html",context)
    
    
def dashboard(req):
    print(req.user)
    username = req.user
    return render(req, "dashboard.html", {"username": username})

def userlogout(req):
    logout(req)
    return redirect('/')