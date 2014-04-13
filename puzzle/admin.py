from django.contrib import admin
from puzzle.models import Puzzle, Dataset, Answer

class AnswerInline(admin.TabularInline):
  model = Answer
  extra = 0

class DatasetInline(admin.StackedInline):
  model = Dataset
  extra = 1
  

class PuzzleAdmin(admin.ModelAdmin):
  inlines = [DatasetInline]
  
class DatasetAdmin(admin.ModelAdmin):
  inlines = [AnswerInline]

admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Answer)