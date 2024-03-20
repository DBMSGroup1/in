from django.http import HttpResponse
from django.shortcuts import render,redirect
import mysql.connector as db
from django.contrib import messages
mydb=db.connect(host='localhost',user='admin',password='6062')
cursor=mydb.cursor()
curr_user=None
loc=[] 
cursor.execute('use test;')
cursor.execute('select station_name from Intercity_project.stations;')
for i in cursor:
    loc.append(i[0])
sched=[]
sql = "select r.route_name , t.train_name, s.station_name , Date , EAT , EDT from train_schedule ts, routes r, trains t , stations s where ts.train_no = t.train_no  and r.route_no=ts.route_no and ts.station_code = s.station_code; "
cursor.execute('use Intercity_project;')
cursor.execute(sql);
for i in cursor:
    sched.append(list(i))
data={'isUser':0,'loc':loc,'sched':sched}
cursor=None
def root():
    global cursor
    mydb=db.connect(host='localhost',user='admin',password='6062')
    cursor=mydb.cursor()

def index(request):
    global curr_user
    uname = request.POST.get('uname',None)
    upass=request.POST.get('pass',None)
    print(uname ,upass)
    if(uname!=None and upass!=None):
        try:
            mydb = db.connect(host='localhost',user=uname,password=upass)
            cursor=mydb.cursor()
            curr_user=uname
            data['isUser']=1  
            messages.success(request,f"Your are Loged in as {curr_user}")  
            return render(request,'homepage.html',data)
        except:
            messages.error(request,'Wrong credentials!')
            return redirect(login)        
    else:
        messages.error(request,'you need to log in!')
        return render(request,'index.html',data)

def login(request):
    global cursor
    name=request.POST.get('name',None)
    uname=request.POST.get('uname',None)
    upass=request.POST.get('pass',None)
    if(name and uname and upass):
        mydb=db.connect(host='localhost',user='admin',password='6062')
        cursor=mydb.cursor()
        try:
            sql=f"create user %s@'localhost' identified by %s";
            val = (uname,upass)
            print(sql,val)
            cursor.execute(sql,val)
            messages.success(request,f'You are successfully Registered !, Please Log in to proceed ')
            return render(request,'login.html')
        except db.Error as err:
            if(err.errno==1396):
                messages.error(request,'user name already used, please try defferent User Name! ')
            else:
                messages.error(request,err)
            return redirect(signup)
    if(name==None and uname==None and upass==None):
        return render(request,'login.html',data)
    else:
        messages.error(request,'All fields are compalsary')
        return redirect(signup)

def signup(request): 
    return render(request,'user_register.html')
def logout(request):
    curr_user=None
    data['isUser']=0
    global cursor
    cursor = None
    return index(request)

def home(request):
    return render(request,'homepage.html',data)
def schedule(request):
    return render(request,'schedule.html',data)
