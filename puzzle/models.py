# encoding: utf8
from django.db import models
import uuid
from django.utils import timezone
from django.contrib import auth

# Create your models here.
class Puzzle(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  def __str__(self):
    return "Puzzle: "+self.title

def solution_upload_to(instance, filename):
  return "solution/d%s_solution_%s.txt"%(instance.pk, uuid.uuid4())

def data_upload_to(instance, filename):
  return "dataset/d%s_data.txt"%(instance.pk)

class Dataset(models.Model):
  puzzle = models.ForeignKey(Puzzle)
  scale = models.CharField(max_length=100)
  score = models.IntegerField(default=10)
  data = models.FileField(upload_to=data_upload_to)
  solution = models.FileField(upload_to=solution_upload_to)
  def __str__(self):
    return self.scale+" Dataset of Puzzle: "+self.puzzle.title

class UserProfile(models.Model):
    STUDENT_TYPE_CHOICES=((0, '社會組(或純練習)'), (1,'高中以下'), (2,'大學/專科'))
    user = models.OneToOneField("auth.User")    
    student_type = models.IntegerField("參加組別", default=0, choices=STUDENT_TYPE_CHOICES)
    desc = models.TextField("簡介：（學校、報名票種、序號等等）")
    score = models.IntegerField(default=0)
    def __str__(self):
      return "User: "+self.user.username
    
def user_upload_output(instance, filename):
  return "user/user%s_d%s_output_%s.txt"%(instance.user.user.pk, instance.dataset.pk, uuid.uuid4())

def user_upload_source(instance, filename):
  return "user/user%s_d%s_src_%s.py"%(instance.user.user.pk, instance.dataset.pk, uuid.uuid4())

class Answer(models.Model):
  readonly_fields = ('result', )
  dataset = models.ForeignKey(Dataset)
  user = models.ForeignKey(UserProfile)
  answer = models.FileField(upload_to=user_upload_output)
  source_code = models.FileField(upload_to=user_upload_source)
  submitted_time = models.DateTimeField('time submitted', default=timezone.now())
  result = models.BooleanField(default = False) 
  def __str__(self):
    return "Answer of (%s) by (%s) "%(self.dataset, self.user)
  
  