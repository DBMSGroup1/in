from django.http import HttpResponse
from django.shortcuts import render,redirect
import mysql.connector as db
from django.contrib import messages
import myhash
mydb=db.connect(host='localhost',user='admin',password='6062')
cursor=mydb.cursor()

# current user name
curr_user=None

#station names for homepage
loc=[] 
cursor.execute('use test;')
cursor.execute('select station_name from Intercity_project.stations;')
for i in cursor:
    loc.append(i[0])

#data for schedule 
sched=[]
sql = "select r.route_name , t.train_name, s.station_name , Date , EAT , EDT from train_schedule ts, routes r, trains t , stations s where ts.train_no = t.train_no  and r.route_no=ts.route_no and ts.station_code = s.station_code; "
cursor.execute('use Intercity_project;')
cursor.execute(sql);
for i in cursor:
    sched.append(list(i))


#data section
data={'isUser':0,'loc':loc,'sched':sched,'uname':''}
cursor=None
usertype='';
is_login=False;


# index page after login
def index(request):
    if(is_login):
        return render(request,'homepage.html',data)
    return redirect(start)

# main page of site
def start(request):
    return render(request,'main.html',data)

#index page for showing login details
def login(request):
    global curr_user
    global usertype
    uname = request.POST.get('uname',None)
    upass=request.POST.get('pass',None)
    print(uname ,upass,"username and pass")
    if( (uname!=None and upass!=None)):
        try:
            mydb=db.connect(host='localhost',user='admin',password='6062')
            cursor=mydb.cursor()
            if(usertype=="users"):
                sql=f"select password,name from Intercity_project.users where user_name= '{uname}';"
            else:
                sql=f"select password,name from Intercity_project.agents where user_name= '{uname}';"

            val=(uname)
            print(sql)
            cursor.execute(sql)
            ps='password'
            tmp='tempData'
            for i in cursor:
                ps=i[0]
                tmp=i[1]
                print(ps)
                print(myhash.myhash(upass))
                print('working fine')
            if(ps==myhash.myhash(upass)):
                curr_user=uname
                data['isUser']=1
                data['uname']=tmp
                return render(request,'homepage.html',data)
            else:
                print('else ->')
                messages.error(request,'Wrong credentials!')
                if(usertype=='users'):
                    return redirect(user_log)        
                return redirect(agent_log)
        except db.Error as er:
            print(er)
            messages.error(request,'Wrong credentials!')
            if(usertype=='users'):
                return redirect(user_log)        
            else:
                return redirect(agent_log)
              
    else:
        messages.error(request,'you need to log in!')
        data['isUser']=0  
        if(usertype=='users'):
                return redirect(user_log)        
        else:
                return redirect(agent_log)
            
        
#log in page for user


def register(request):
    global mydb
    global usertype
    name=request.POST.get('name',None)
    uname=request.POST.get('uname',None)
    upass=request.POST.get('pass',None)
    mail=request.POST.get('mail',None)
    contact=request.POST.get('contact',None)
    address=request.POST.get('address',None)

    if(name and uname and upass):
        mydb=db.connect(host='localhost',user='admin',password='6062')
        cursor=mydb.cursor()
        try:
            #mysql> insert into users(user_name,name,Mail,contact,Address,password) values('Kunal','Kunal Ranaware','kunal@gmail.com','1234567890','Pune','1456001954136179839');
            if(usertype=="users"):    
                sql=f"insert into Intercity_project.users(user_name,name,Mail,contact,Address,password) values(%s,%s,%s,%s,%s,%s)";
            else:
                sql=f"insert into Intercity_project.agents(user_name,name,Mail,contact,Address,password) values(%s,%s,%s,%s,%s,%s)";
            val = (uname,name,mail,contact,address,myhash.myhash(upass))
            print(sql,val)
            cursor.execute(sql,val)
            messages.success(request,f'You are successfully Registered !, Please Log in to proceed ')
            mydb.commit()
            if(usertype=='users'):
                return redirect(user_log)
            else:
                return redirect(agent_log)            
        except db.Error as err:
            if(err.errno==1396):
                messages.error(request,'user name already used, please try defferent User Name! ')
            else:
                messages.error(request,err)
            if(usertype=='users'):
                return redirect(user_reg)
            else:
                return redirect(agent_reg)
    if(name==None and uname==None and upass==None):
        return render(request,'login.html',data)
    else:
        messages.error(request,'All fields are compalsary')
        if(usertype=='users'):
            return redirect(user_reg)
        else:
            return redirect(agent_reg)


def user_log(request):
    global usertype;
    usertype='users';
    return render(request,'login.html');

def agent_log(request):
    global usertype;
    usertype='agent';
    return render(request,'agent_login.html');

#signup for user
def user_reg(request): 
    global usertype;
    usertype='users';
    return render(request,'user_register.html')

#signup for agent
def agent_reg(request): 
    global usertype
    usertype='agent'
    return render(request,'agent_register.html')


#logout for user
def logout(request):
    curr_user=None
    is_login=False
    data['isUser']=0
    global cursor
    cursor = None
    return redirect(start)

# home page 
def home(request):
    if(data['isUser']==1):
        return render(request,'homepage.html',data)
    else:
        return redirect(index)

#schedule page
def schedule(request):
    return render(request,'schedule.html',data)
