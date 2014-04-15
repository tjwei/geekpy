from django.contrib import admin
from puzzle.models import Puzzle, Dataset, Answer, PuzzleCollection

class AnswerInline(admin.TabularInline):
  model = Answer
  extra = 0

class DatasetInline(admin.StackedInline):
  model = Dataset
  extra = 1
  
class PuzzleInline(admin.StackedInline):
  model = Puzzle
  extra = 3

class PuzzleCollectionAdmin(admin.ModelAdmin):
  inlines = [PuzzleInline]

class PuzzleAdmin(admin.ModelAdmin):
  inlines = [DatasetInline]
  
class DatasetAdmin(admin.ModelAdmin):
  inlines = [AnswerInline]

admin.site.register(PuzzleCollection, PuzzleCollectionAdmin)
admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Answer)
