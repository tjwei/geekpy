from django.contrib import admin
from puzzle.models import Puzzle, Dataset, Answer, PuzzleCollection, UserProfile

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

class AnswerAdmin(admin.ModelAdmin):
  list_display = ('user', 'dataset', 'result', 'submitted_time', 'answer')  
class DatasetAdmin(admin.ModelAdmin):
  inlines = [AnswerInline]

admin.site.register(PuzzleCollection, PuzzleCollectionAdmin)
admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Answer, AnswerAdmin)

from mezzanine.accounts.admin import UserProfileAdmin
from django.contrib.auth.models import User

class MyProfileAdmin(UserProfileAdmin):
    list_display = UserProfileAdmin.list_display+("student_type", )
    def student_type(self, instance):
        return instance.profile.student_type
admin.site.unregister(User)
admin.site.register(User, MyProfileAdmin)
