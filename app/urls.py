from django.http import request
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.index,name='index'),
   path('rpage/',views.registerpage,name='registerpage'),
   path('login/',views.loginstudent,name='loginpage'),
   path('tlogin',views.Tuterlogin,name='loginTutor'),
   path('tregister/',views.Tutorregister,name='registerTutor'),
   path('rstudent/',views.registerstudent,name='registerstudent'),
   path('otpstudent/',views.otpstudent,name='otpstudent'),
   path('rtutor/',views.registertutor,name='registertutor'),
   path('otptutor/',views.otptutor,name='otptutor'),
   path('loginvarifyS/',views.loginvarifyS,name='loginvarifyS'),
   path('loginvarifyT/',views.loginvarifyT,name='loginvarifyT'),
   path('indexTutor/',views.indexTutor,name='indexTutor'),
   path('sprofile/',views.student_profile,name='student_profile'),
   path('sdata/<int:pk>',views.student_data,name='student_data'),
   path('tprofile/',views.Tutor_profile,name='Tutor_profile'),
   path('tdata/<int:pk>',views.Tutor_data,name='Tutor_data'),
   path('logouts/',views.studentlogout,name='studentlogout'),
   path('logoutT',views.tutorlogout,name='tutorlogout'),
   path('home/',views.index1,name='index1'),
   path('contactUs/',views.contactus,name='contactus'),

   #####################--Tutor--######################
   path('addcourse/',views.addcourse,name='addcourse'),
   path('coursedata/',views.coursedata,name='coursedata'),
   path('homepage/',views.homepage,name='homepage'),

   ####################----course----###################
   path('shopgrid/',views.shopgrid,name='shopgrid'),
   path('allcourses/',views.allcourses,name='allcourses'),
   path('class_grid/',views.class_grid,name='class_grid'),
   path('course_detail/<int:pk>',views.course_detail,name='course_detail'),
   path('editcourse/<int:pk>',views.editcourse,name='editcourse'),
   path('edit_coursedata/<int:pk>',views.edit_coursedata,name='edit_coursedata'),
   path('reviews/<int:pk>',views.reviews,name='reviews'),

   ####################-----Cart-----######################
   path('cart_gen/',views.cart_gen,name='cart_gen'),
   path('cart/<int:pk>',views.cart,name='cart'),
   path('cremove/<int:pk>',views.cremove,name='cremove'),
   path('all_coursesT/',views.all_coursesT,name='all_coursesT'),
   path('all_studentsT/<int:pk>',views.all_studentsT,name='all_studentsT'),
   path('checkout/',views.checkout,name='checkout'),

   ##################-----Payment---#########################
   path('pay/',views.initiate_payment,name='pay'),
   path('callback/',views.callback,name='callback'),
   # path('welcomeback/',views.welcome,name='welcome'),
]
