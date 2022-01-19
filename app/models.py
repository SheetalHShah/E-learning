from operator import mod
from statistics import mode
from django.db import models

# Create your models here.
class User(models.Model):
    Username = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Role =  models.CharField(max_length=50)
    OTP = models.IntegerField()
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now_add=True)
    is_varified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # def __str__(self):
    #     return self.Username


class Student1(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    Contact = models.CharField(max_length=50)
    Skills = models.CharField(max_length=50)
    Qualification = models.CharField(max_length=50)
    Experience = models.CharField(max_length=50)
    DOB = models.DateField(default="2020-05-01")
    Country = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Profile_Pic = models.ImageField(upload_to="img/",default='abc.jpg')
    #def __str__(self):
     #   return self.Firstname

class Tutor1(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Gender = models.CharField(max_length=50)
    Contact = models.CharField(max_length=50)
    Skills = models.CharField(max_length=50)
    Qualification = models.CharField(max_length=50)
    Experience = models.CharField(max_length=50)
    DOB = models.DateField(default="2020-05-01")
    Country = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Profile_Pic = models.ImageField(upload_to="img/",default='abc.jpg')
    # def __str__(self):
    #     return self.Firstname

class Category(models.Model):
    Name = models.CharField(max_length=50)
    is_created = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True)
    # def __str__(self):
    #     return self.Name


class Course1(models.Model):
    Tutor_id = models.ForeignKey(Tutor1,on_delete=models.CASCADE)
    Category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Code = models.IntegerField()
    Description = models.CharField(max_length=100)
    Duration = models.CharField(max_length=50)
    Price = models.IntegerField()
    Technology = models.CharField(max_length=50)
    Pre_Requirement = models.CharField(max_length=50)
    course_pic = models.ImageField(upload_to="img/",default="abc.jpg")
    is_created = models.DateTimeField(auto_now_add=True)
    is_update = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    Course_id = models.ForeignKey(Course1,on_delete=models.CASCADE)
    Student_id = models.ForeignKey(Student1,on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

class review(models.Model):
    course_id = models.ForeignKey(Course1,on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student1,on_delete=models.CASCADE)
    r_name = models.CharField(max_length=50)
    r_email = models.EmailField(max_length=50)
    r_content = models.CharField(max_length=1000)


