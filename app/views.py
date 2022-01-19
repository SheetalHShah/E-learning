from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models.deletion import CASCADE
from django.db.models.fields import CommaSeparatedIntegerField
from django.http import request
from django.shortcuts import render,redirect
from django.urls.resolvers import get_resolver
from .models import *
from random import randint
from .utils import *
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
import socket
socket.getaddrinfo('localhost',8080)
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request,'app/index.html')

def index1(request):
    try:
        if request.session['Role'] == 'Tutor':
            del request.session['Email']
            del request.session['id']
            del request.session['Password']
            request.session.modified = True
            return render(request,'app/index.html')
        else:
            return render(request,'app/index.html')
    except:
        return render(request,'app/index.html')

def indexTutor(request):
    # return render(request,'app/Tutor/index-2.html')
    tid = request.session['id']
    tdata = Tutor1.objects.get(user_id = tid)
    print('------------------------------------',tid)
    cdata = Course1.objects.filter(Tutor_id = tdata.id)
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',cdata)
    j=len(cdata)
    totals=0
    totalf=0
    for i in cdata:
        crdata = Cart.objects.filter(Course_id=i)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^',crdata)
        totals+=len(crdata)
        for k in crdata:
            totalf +=k.total
            print('***************Total =  ',totalf)
    return render(request,'app/Tutor/index-2.html',{'key1':tdata,'noc':j,'totals':totals,'totalf':totalf})

def registerpage(request):
    return render(request,'app/registerstudent.html')

def loginstudent(request):
    return render(request,'app/loginstudent.html')

def Tuterlogin(request):
    return render(request,'app/Tutorlogin.html')

def Tutorregister(request):
    return render(request,'app/TutorRegister.html')

def registerstudent(request):
    if request.POST['role'] == 'Student':
        role = request.POST['role']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['psw']
        cpassword = request.POST['psw-repeat']
        contact = request.POST['contact']

        echeck = User.objects.filter(Email=email)
        if echeck:
            msg = 'User already exist'
            return render(request,'app/registerstudent.html',{'msg':msg})

        else:
            if password == cpassword :
                otp = randint(10000,99999)
                ddata = User.objects.create(Username = name,Email = email,Password = password,Role = role,OTP = otp)
                sdata = Student1.objects.create(user_id = ddata,Firstname = name,Contact = contact)
                email_subject = "Student email : Account Verification"
                sendmail(email_subject,'mail_template',email,{'name':name,'otp':otp,'link':'http://localhost:8000/rstudent/'})
                # sdata = Student1.objects.create(user_id = ddata,Firstname = name,Contact = contact)
                return render(request,'app/otpvarify.html',{'email':email,'OTP':otp})

            else:
                msg = 'Please provide same password'
                return render(request,'app/registerstudent.html',{'msg':msg})

def otpstudent(request):
    hotp = request.POST['otp_var']
    email = request.POST['email']
    otp = request.POST['otp']

    user = User.objects.get(Email = email)
    if user:
        uotp = user.OTP
        cotp = otp
        if str(uotp) == str(cotp):
            print('varified')
            return render(request,'app/loginstudent.html')
        else:
            msg = 'OTP does not match'
            return render(request,'app/otpvarify.html',{'msg':msg})
    else:
        message = 'User does not exist'
        return render(request,'app/registerstudent.html',{'msg':message})

def registertutor(request):
    if request.POST['role'] == 'Tutor':
        role = request.POST['role']
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        password = request.POST['psw']
        cpassword = request.POST['psw-repeat']

        echeck = User.objects.filter(Email=email)
        if echeck:
            msg = 'User already exist'
            return render(request,'app/TutorRegister.html',{'msg':msg})
        else:
            if password == cpassword :
                otp = randint(10000,99999)
                ddata = User.objects.create(Username = name,Email = email,Password = password,Role = role,OTP = otp)
                #ddata = User.objects.create(Username = name,Email = email,Password = password,Role = role,OTP = otp)
                sdata = Tutor1.objects.create(user_id = ddata,Contact = contact)
                return render(request,'app/otpvarifyTutor.html',{'email':email,'OTP':otp})
                #return render(request,'app/otpvarify.html',{'email':email,'OTP':otp})
            else:
                msg = 'Please provide same password'
                return render(request,'app/TutorRegister.html',{'msg':msg})
        
def otptutor(request):
    hotp = request.POST['otp_var']
    email = request.POST['email']
    otp = request.POST['otp']

    user = User.objects.get(Email = email)
    if user:
        uotp = user.OTP
        cotp = otp
        if str(uotp) == str(cotp):
            print('varified')
            return render(request,'app/Tutorlogin.html')
        else:
            msg = 'OTP does not match'
            return render(request,'app/otpvarifyTutor.html',{'msg':msg})
    else:
        message = 'User does not exist'
        return render(request,'app/TutorRegister.html',{'msg':message})

def loginvarifyS(request):
    if request.POST['role'] == 'Student':
        email = request.POST['email']
        password = request.POST['psw']
        try:
            user = User.objects.get(Email = email)
        except:
            msg = 'please register yourself'
            return render(request,'app/registerstudent.html',{'msg':msg})

        if user:
            if user.Password == password and user.Role == 'Student':
                request.session['Role'] = user.Role
                request.session['id'] = user.id
                request.session['Password'] = user.Password
                request.session['Username'] = user.Username
                request.session['Email'] = user.Email
                name = user.Username
                #return redirect('index')
                return render(request,'app/index.html',{'name':name})
            else:
                msg = 'please provide valid password'
                return render(request,'app/loginstudent.html',{'msg':msg})
        else:
            return render(request,'app/registerstudent.html')

def loginvarifyT(request):
    if request.POST['role'] == 'Tutor':
        email = request.POST['email']
        password = request.POST['psw']
        try:
            user = User.objects.get(Email = email)
        except:
            msg = 'please register yourself'
            return render(request,'app/TutorRegister.html',{'msg':msg})
        if user:
            if user.Password == password and user.Role == 'Tutor':
                request.session['Role'] = user.Role
                request.session['id'] = user.id
                request.session['Password'] = user.Password
                request.session['Username'] = user.Username
                request.session['Email'] = user.Email
                tid = request.session['id']
                tdata = Tutor1.objects.get(user_id = tid)
                print('------------------------------------',tid)
                cdata = Course1.objects.filter(Tutor_id = tdata.id)
                print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',cdata)
                j=len(cdata)
                totals=0
                totalf=0
                for i in cdata:
                    crdata = Cart.objects.filter(Course_id=i)
                    print('^^^^^^^^^^^^^^^^^^^^^^^^^^',crdata)
                    totals+=len(crdata)
                    for k in crdata:
                        totalf +=k.total
                    print('***************Total =  ',totalf)
                return render(request,'app/Tutor/index-2.html',{'key1':tdata,'noc':j,'totals':totals,'totalf':totalf})
            else:
                msg = 'please provide valid password'
                return render(request,'app/Tutorlogin.html',{'msg':msg})
        else:
            return render(request,'app/TutorRegister.html')

def student_profile(request):
    sid = request.session['id']
    print('*********************',sid,'***************************')
    sdata = Student1.objects.get(user_id = sid)
    print('##################################',sdata)
    return render(request,'app/student_profile.html',{'key1':sdata})
    

def student_data(request,pk):
    udata = User.objects.get(id = pk)
    if udata.Role == "Student":
        sdata = Student1.objects.get(user_id=udata)
        #print('***************',udata.Email,'*****************')
        #print(request.FILES['Pic'])
        sdata.Firstname = request.POST['firstname']
        sdata.Lastname = request.POST['lastname']
        sdata.Email = request.POST['email']
        sdata.Contact = request.POST['contact']
        sdata.Address = request.POST['address']
        sdata.Gender = request.POST['gender']
        sdata.Qualification = request.POST['qualification']
        sdata.DOB = request.POST['DOB']
        sdata.Country = request.POST['country']
        sdata.State = request.POST['state']
        sdata.City = request.POST['city']
        try:
            sdata.Profile_Pic = request.FILES['Pic']
            sdata.save()
            name = udata.Username
            return render(request,'app/index.html',{'name':name})
        except:
            sdata.save()
            name = udata.Username
            return render(request,'app/index.html',{'name':name})
        #return render(request,'app/index.html')

def Tutor_profile(request):
    tid =  request.session['id']
    tdata = Tutor1.objects.get(user_id=tid)
    return render(request,'app/Tutor/Tutor_profile.html',{'key1':tdata})

def Tutor_data(request,pk):
    udata = User.objects.get(id = pk)
    if udata.Role == "Tutor":
        tdata = Tutor1.objects.get(user_id=udata)
        #print('***************',request.POST['email'],'*****************')
        tdata.Firstname = request.POST['firstname']
        tdata.Lastname = request.POST['lastname']
        tdata.Email = request.POST['email']
        tdata.Contact = request.POST['contact']
        tdata.Address = request.POST['address']
        tdata.Gender = request.POST['gender']
        tdata.Qualification = request.POST['qualification']
        tdata.DOB = request.POST['DOB']
        tdata.Country = request.POST['country']
        tdata.State = request.POST['state']
        tdata.City = request.POST['city']
        cdata = Course1.objects.filter(Tutor_id = tdata.id)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',cdata)
        j=len(cdata)
        totals=0
        totalf=0
        for i in cdata:
            crdata = Cart.objects.filter(Course_id=i)
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^',crdata)
            totals+=len(crdata)
            for k in crdata:
                totalf +=k.total
                print('***************Total =  ',totalf)
        try:
            tdata.Profile_Pic = request.FILES['Pic']
            tdata.save()
            # return render(request,'app/Tutor/index-2.html')
            return render(request,'app/Tutor/index-2.html',{'key1':tdata,'noc':j,'totals':totals,'totalf':totalf})
        except:
            tdata.save()
            # return render(request,'app/Tutor/index-2.html')
            return render(request,'app/Tutor/index-2.html',{'key1':tdata,'noc':j,'totals':totals,'totalf':totalf})
        
    
def studentlogout(request):
    del request.session['Email']
    del request.session['Password']
    del request.session['id']
    request.session.modified = True
    return render(request,'app/index.html')

def tutorlogout(request):
    del request.session['Email']
    del request.session['Password']
    del request.session['id']
    request.session.modified = True
    return render(request,'app/index.html')

def contactus(request):
    return render(request,'app/contact.html')

def addcourse(request):
    catdata = Category.objects.all()
    return render(request,'app/Tutor/add-courses.html',{'catname':catdata})

def coursedata(request):
    id = request.session['id']
    tid = Tutor1.objects.get(user_id = id)
    cname = request.POST['category']
    catid = Category.objects.get(id=cname)
    coursename = request.POST['coursename']
    coursecode = request.POST['coursecode']
    coursedetail = request.POST['coursedetail']
    cduration = request.POST['cduration']
    cprice = request.POST['cprice']
    ctechnology = request.POST['ctechnology']
    cpre_req = request.POST['cpre_req']
    cpic = request.FILES['cpic']
    cdata = Course1.objects.create(Tutor_id = tid,Category_id = catid,Name = coursename,Code = coursecode,Description = coursedetail,Duration = cduration,Price = cprice, Technology = ctechnology,Pre_Requirement = cpre_req,course_pic = cpic)
    msg = "Course added..."
    return render(request,'app/Tutor/index-2.html',{'msg':msg})

def shopgrid(request):
    try:
        if request.session['id'] and request.session['Email']:
            cdata = Course1.objects.all()
            return render(request,'app/shop-grid.html',{'course':cdata})
    except:
        cdata = Course1.objects.all()
        return render(request,'app/shop-grid.html',{'course':cdata})

def allcourses(request):
    id = request.session['id']
    print('!!!!!!!!!!!!!!!!!!!!!!',id)
    tid = Tutor1.objects.get(user_id = id)
    print('*********************',tid)
    cid = Course1.objects.filter(Tutor_id = tid)
    print('+++++++++++++++++++++',cid)
    if tid:
         return render(request,'app/Tutor/all-courses1.html',{'course':cid})
    else:
        return render(request,'app/Tutor/index-2.html')

def class_grid(request):
    try:
        if request.session['id'] and request.session['Email']:
            cdata = Course1.objects.all()
            return render(request,'app/class-grid.html',{'course':cdata})
    except:
        cdata = Course1.objects.all()
        return render(request,'app/class-grid.html',{'course':cdata})

def course_detail(request,pk):
    print(pk)
    cdata = Course1.objects.get(id=pk)
    print('**********************',cdata.Tutor_id_id)
    tdata = Tutor1.objects.get(id=cdata.Tutor_id_id)
    print('######################',tdata)
    return render(request,'app/class-details.html',{'course':cdata,'tdata':tdata})
   
def reviews(request,pk):
    firstname = request.POST['name']
    email = request.POST['email']
    content = request.POST['content']
    print(pk)
    try:
        id = request.session['id']
        print(id)
        udata = User.objects.get(id=id)
        print('user data-------------------',udata)
        sdata = Student1.objects.get(user_id=udata)
        print('student data---------------',sdata)
        cdata = Cart.objects.filter(Student_id = sdata)
        print('cart data---------------------------',cdata)
        if id:
            if udata.Role == 'Student' and udata.Email == email:
                print("hello")
                for i in cdata:
                    print(i.Student_id)
                    if i.Course_id == pk and i.Student_id == sdata:
                        print('in--------------------------')
                        rdata = review.objects.create(course_id=i.Course_id,student_id=i.Student_id,r_name=firstname,r_email=email,r_content=content)
                        rdata.save()
                        print(rdata)
                        msg = "your review has been added..."
                        return render(request,'app/class-details.html',{'msg':msg})    
                    else:
                        pass
                # return render(request,'app/class-details.html',{'msg':'your review has been added...'})    
            else:
                msg = 'please login yourself first as student...'
                print('############----------------#############')
                return render(request,'app/index.html',{'msg':msg})    
        else:
            msg = 'please login yourself first in outer else...'
            print('############----------------#############')
            return render(request,'app/index.html',{'msg':msg})
    except:
        msg = 'please login yourself first in except...'
        print('############----------------#############')
        return render(request,'app/index.html',{'msg':msg})

    
def homepage(request):
    del request.session['Email']
    del request.session['Password']
    del request.session['id']
    request.session.modified = True
    return render(request,'app/index.html')

def editcourse(request,pk):
    #tid = request.session['id']
    cdata = Course1.objects.get(id=pk)
    #return render(request,'app/Tutor/edit-courses.html')
    return render(request,'app/Tutor/edit-courses.html',{'key':cdata})

def edit_coursedata(request,pk):
    # print('***********************************',request.session['id'])
    print('***********************************',pk)
    # tdata = Tutor1.objects.get(user_id = pk)
    cdata = Course1.objects.get(id=pk)
    #tdata.Firstname = request.POST['firstname']
    if cdata:
        cdata.Name = request.POST['coursename']
        cdata.Code = request.POST['coursecode']
        cdata.Description = request.POST['coursedetail']
        cdata.Duration = request.POST['courseduration']
        cdata.Price = request.POST['courseprice']
        cdata.Firstname = request.POST['tutorname']
        try:
            cdata.course_pic = request.FILES['coursepic']
            cdata.save()
            return render(request,'app/Tutor/index-2.html')
        except:
            cdata.save()
            return render(request,'app/Tutor/index-2.html')
        
        return render(request,'app/Tutor/index-2.html')
    # return render(request,'app/Tutor/edit-courses.html',{'key1':cdata})

def cart_gen(request):
    try:
        if request.session['id'] and request.session['Email']:
            if request.session['Role'] == 'Tutor':
                msg = 'Please Register Yourself First as Student'
                cdata = Course1.objects.all()
                return render(request,'app/shop-grid',{'course':cdata,'msg':msg})
            sid = request.session['id']
            print(sid)
            print('Login---------------------------')
            sdata = Student1.objects.get(user_id=sid)
            print(sdata)
            cartd = Cart.objects.filter(Student_id = sdata)
            if len(cartd)==0:
                msg='Your cart is empty!'
                return render(request,'app/index.html',{'msg':msg})
            print(cartd)
            tprice = 0
            for i in cartd:
                print(i)
                tprice += i.total
                # return render(request,'app/cart.html',{'crdata':cartd,'tprice':tprice,'msg':''})
            return render(request,'app/cart.html',{'tprice':tprice,'crdata':cartd,'msg':''})
        else:
            # msg = 'Please Login Yourself First else in cart_gen'
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            cdata = Course1.objects.all()
            return render(request,'app/shop-grid.html',{'course':cdata})
            # return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})
    except:
        msg = 'Please Login Yourself First...'
        print('############----------------#############')
        return render(request,'app/index.html',{'msg':msg})

def cart(request,pk):
    try:
        if request.session['id'] and request.session['Email']:
            if request.session['Role'] == 'Tutor':
                msg = 'Please Login Yourself First as Student...'
                cdata = Course1.objects.all()
                return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})
            sid = request.session['id']
            print(sid)
            print('Login-----------------------------')
            sdata = Student1.objects.get(user_id = sid)
            print('***************************',sdata)
            cdata = Course1.objects.get(id = pk)
            print(cdata.id)
            try:
                scdata = Cart.objects.filter(Student_id=sdata)
                print('###########################################',scdata)
                for i in scdata:
                    print('in for course id ',i.Course_id)
                    print(cdata)
                    if i.Course_id == cdata:
                        msg = 'The Item Is Already Added'
                        cdata = Course1.objects.all()
                        return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})
                # ddata = Cart.objects.get(Course_id_id = cdata.id)
                # print(ddata)
                # msg = 'The Item Is Already Added'
                # cdata = Course1.objects.all()
                # print(cdata)
                sheetal
                return render(request,'app/shop-grid.html',{'course':cdata,'msg':'msg'})
            except:
                cartdata = Cart.objects.create(Course_id = cdata,Student_id = sdata,total = cdata.Price,subtotal = cdata.Price)
                cartd = Cart.objects.filter(Student_id = sdata)
                print('&&&&&&&&&&&&&&&&&&&&&',cartd)
                tprice = 0
                for i in cartd:
                    print('--------------------------------------------')
                    tprice += i.total
                print(tprice)
                msg = 'Item added in the cart'
                return render(request,'app/cart.html',{'crdata':cartd,'tprice':tprice,'msg':'msg'})
        else:
            # msg = "Please login yourself first..."
            print('****************************')
            cdata = Course1.objects.all()
            return render(request,'app/shop-grid.html',{'course':cdata})
    except:
        msg = "Please login yourself first..."
        print('*********####################********')
        cdata = Course1.objects.all()
        return render(request,'app/shop-grid.html',{'course':cdata,'msg':msg})

def cremove(request,pk):
    print('****************',pk)
    cd = Cart.objects.get(id=pk).delete()
    sid = request.session['id']
    print(sid)
    # print('Login-----------------------------')
    sdata = Student1.objects.get(user_id = sid)
    # print('***************************',sdata)
    cartd = Cart.objects.filter(Student_id = sdata)
    
    
    return render(request,'app/cart.html',{'crdata':cartd})


def all_coursesT(request):
    #tid = request.session['id']

    return render(request,'app/Tutor/all-courses1.html')

def all_studentsT(request,pk):
    udata = User.objects.get(id=pk)
    tutor = Tutor1.objects.get(user_id = udata)
    cdata = Course1.objects.filter(Tutor_id = tutor)
    coursename = []
    Scourse = []
    crt = 0
    for course in cdata:
        coursename.append(course.Name)
        try:
            crt = Cart.objects.all().filter(Course_id_id = course)
            Scourse.append(crt)
        except:
            pass
    return render(request,'app/Tutor/all-students.html',{'sdata':crt,'Scourse1':Scourse})



    # id1 = request.session['id']
    # tid = Tutor1.objects.get(user_id=id1)
    # print('Tutor id = ',tid)
    # # alls=[]
    # allc=[]
    # # dict1={}
    # cdata = Course1.objects.filter(Tutor_id=tid)
    # print('------------------Course Data',cdata)
    # for i in cdata:
    #     cartd = Cart.objects.filter(Course_id=i)
    #     print('*********************************',cartd)
    #     if len(cartd)!=0:
    #         # salls=[]
    #         for j in cartd:
    #             if j.Course_id not in allc:
    #                 allc.append(j.Course_id)
    #             else:
    #                 pass
    #             sdata = Student1.objects.get(id=j.Student_id_id)
    #             alls.append(sdata)
    #             # salls.append(sdata)
    #         # alls.append(salls)
    #     else:
    #         pass
    # for i in cdata:
    #     try:
    #         crdata = Cart.objects.all().filter(Course_id = i)
    #         allc.append(crdata)    
    #     except:
    #         pass

    # print('.....................all courses = ',allc)
    # for i in allc:
    #     print('#$#$#$#$#$#$#$#$#$#$#$$#$#$#$#',i)
    # # print('##########################',alls)

    # return render(request,'app/Tutor/all-students.html',{'allc':allc})
    
def checkout(request):
    sid = request.session['id']
    sdata = Student1.objects.get(user_id=sid)
    cartd = Cart.objects.filter(Student_id=sdata)
    tprice=0
    for i in cartd:
        tprice+=i.total
    request.session['Total'] = tprice
    return render(request,'app/checkout.html',{'sdata':sdata,'cartd':cartd,'tprice':tprice})

#-------------------Payment-------------------

def initiate_payment(request):
    try:
        udata = User.objects.get(Email=request.session['Email'])
        # amount = int(request.POST['tp'])
        amount = request.session['Total']
        print('**************************',amount)
        #amount = int(pk)
        #user = authenticate(request, username=username, password=password)
    except Exception as err:
        print(err)
        return render(request,'app/cart.html',context={'error':'Wrong Account Detail or amount'})
    transaction = Transaction.objects.create(made_by=udata, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY
    # if request.method == "GET":
    #     return render(request, 'payments/pay.html')
    # try:
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     amount = int(request.POST['amount'])
    #     user = authenticate(request, username=username, password=password)
    #     if user is None:
    #         raise ValueError
    #     auth_login(request=request, user=user)
    # except:
    #     return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

    # transaction = Transaction.objects.create(made_by=user, amount=amount)
    # transaction.save()
    # merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'app/redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app/callback.html', context=received_data)
        return render(request, 'app/callback.html', context=received_data)
