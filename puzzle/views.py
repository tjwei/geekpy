# encoding: utf8
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.utils.timezone import utc
# Create your views here.
from puzzle.models import Puzzle, Dataset, Answer, UserProfile, PuzzleCollection

from datetime import datetime
COOL_DOWN_TIME = 300
#TIME_START = datetime(2014,4,18, 17,  tzinfo=timezone.get_current_timezone())
#TIME_END = datetime(2024,4,20, 23, 59, tzinfo=timezone.get_current_timezone())
TIME_START = datetime(2014,6,20, 17,  tzinfo=timezone.get_current_timezone())
TIME_END = datetime(2014,6,22, 23, 59, tzinfo=timezone.get_current_timezone())
COLLECTION=PuzzleCollection.objects.get(title=u"第一次競賽")
COLLECTION2=PuzzleCollection.objects.get(title=u"測試")
COLLECTION3=PuzzleCollection.objects.get(title=u"蟒極客第二次競賽")
COLLECTIONS=[COLLECTION, COLLECTION2]
PUZZLES = COLLECTION.puzzle_set
PUZZLES2 = COLLECTION2.puzzle_set
PUZZLES3 = COLLECTION3.puzzle_set
def game_open():
  return TIME_START <= timezone.now() <= TIME_END

def index(request, pk, force_open=False):
  try:
    user= request.user.profile
  except:
    user = None
  puzzle, puzzle_ds = None, []
  puzzle_list = PUZZLES3.all() if game_open() else set()
  if pk:
    try:
      puzzle = puzzle_list.get(pk=pk)
    except:
      pass
  info=str(user)+"\n"
  rtn = []  
  for p in puzzle_list:
    datas=[]
    for d in p.dataset_set.all():     
      try:
        sol = user.answer_set.get(dataset=d)
      except:	
         sol = None
      if sol:
          timediff = datetime.utcnow().replace(tzinfo=utc)-sol.submitted_time
          cdtime = max(COOL_DOWN_TIME-int(timediff.total_seconds()), 0)
      else:
          cdtime = 0
      datas.append((d, sol, cdtime))
    rtn.append( (p, datas))
    if p == puzzle:
      puzzle_ds = datas
  context = { "puzzle_list" : rtn, "info": info, "puzzle": puzzle, "puzzle_ds": puzzle_ds, "game_open": game_open() or force_open,
	     "TIME_START":TIME_START, "TIME_END": TIME_END}  
  return render(request, "puzzle/index.html", context)

def index0(request, pk, force_open=False):
  try:
    user= request.user.profile
  except:
    user = None
  puzzle, puzzle_ds = None, []
  puzzle_list = PUZZLES.all()|PUZZLES2.all() if game_open() else set()
  if pk:
    try:
      puzzle = puzzle_list.get(pk=pk)
    except:
      pass
  info=str(user)+"\n"
  rtn = []  
  for p in puzzle_list:
    datas=[]
    for d in p.dataset_set.all():     
      try:
        sol = user.answer_set.get(dataset=d)
      except:	
         sol = None
      if sol:
          timediff = datetime.utcnow().replace(tzinfo=utc)-sol.submitted_time
          cdtime = max(COOL_DOWN_TIME-int(timediff.total_seconds()), 0)
      else:
          cdtime = 0
      datas.append((d, sol, cdtime))
    rtn.append( (p, datas))
    if p == puzzle:
      puzzle_ds = datas
  context = { "puzzle_list" : rtn, "info": info, "puzzle": puzzle, "puzzle_ds": puzzle_ds, "game_open": game_open() or force_open,
	     "TIME_START":TIME_START, "TIME_END": TIME_END}  
  return render(request, "puzzle/index.html", context)

def toplist(request, n):  
  l = UserProfile.objects.order_by('-score')
  if n:
    l = l[:n]
  html = "<table width='100%'><tbody>"
  html+=u"<tr  style='background-color: #aaa' ><th>名次</th><th> ID</th><th>分數</th></tr>"
  for i, u in enumerate(l):
    html += "<tr><td style='background-color: #ddd'>%d</td><td  >%s</td><td style='background-color: #ddd'>%d</td></tr>"%(i+1, u.user.username, u.score/1000000)
  html += "</tbody</table>"  
  return HttpResponse(html)


class PuzzleDetailView(generic.DetailView):
  template_name = "puzzle/puzzle_detail.html"
  model = Puzzle

def check_ans(f1, f2):
  f1.open()
  f2.open()  
  rtn = True
  while 1:
      l1 = f1.readline()      
      try:
	l2 = f2.readline()
      except:
	rtn = False
	break      
      if not l1: break
      if not l2:
	rtn = False
	break      
      if l1.rstrip().split()  !=l2.rstrip().split():
	rtn =  False
	break
  f1.close()
  f2.close()
  return rtn
import os
def del_file(f):
  try:
    if os.path.isfile(f.path):
      os.remove(f.path)
      f.delete()
  except:
    pass
	  


def submit(request, pk):
  if not game_open():
    return HttpResponse("Sorry, the game is closed")  
  d = get_object_or_404(Dataset, pk = pk)  
  user= request.user.profile
  result = check_ans(d.solution,  request.FILES['output'])
  ans, new = user.answer_set.get_or_create(dataset=d)    
  if new or not ans.result:
      if not new:
        timediff = timezone.now() - ans.submitted_time
        secs = timediff.total_seconds()
        if secs < COOL_DOWN_TIME:
            return HttpResponse("Please wait for cool down.%f secs"%(300-secs))
	del_file(ans.answer)
	del_file(ans.source_code)
      ans.dataset = d
      ans.answer=request.FILES['output']
      ans.source_code=request.FILES['source']
      ans.submitted_time = timezone.now()
      ans.result = result
      ans.save()
      if result:
	timedelta = (timezone.now() - TIME_START).total_seconds()
        user.score = 10**6*(sum(x.dataset.score for x in user.answer_set.filter(result=True) if x.dataset.puzzle.collection == COLLECTION3)+1) - timedelta
        user.save()
  return HttpResponseRedirect(reverse("puzzle:puzzle", args=(d.puzzle.pk,)))


def del_answer(request, pk):
  if not game_open():
    return HttpResponse("Sorry, the game is closed")
  d = get_object_or_404(Dataset, pk = pk)  
  user= request.user.profile
  try:
    ans = user.answer_set.get(dataset=d)
  except:
    return HttpResponse("本題尚未作答，無法刪除")
  ans.delete()
  timedelta = (timezone.now() - TIME_START).total_seconds()
  user.score = 10**6*(sum(x.dataset.score for x in user.answer_set.filter(result=True) if x.dataset.puzzle.collection==COLLECTION3)+ 1) - timedelta
  user.save()
  return HttpResponseRedirect(reverse("puzzle:puzzle", args=(d.puzzle.pk,)))

