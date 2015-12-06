from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json

from .models import User, Level, Question, Hint

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['user_id','screen_name']
    list_display = ('user_id','screen_name')
    readonly_fields = ('user_id',)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('strLevel', 'enabled')
    actions = ['generate_level_json']

    def generate_level_json(self, request, queryset):
        levelDicts = {}
        for level in queryset:
            strLevel = 'level%d' % level.level
            questions = Question.objects.filter(level=level.level)
            questionsDict = {}
            hintsDict = {}
            for index, q in enumerate(questions):
                # print( 'Level' + str(q.level) + ':' + q.answer)
                questionDict = {
                    "image": q.question_id,
                    "answered": False,
                    "answer": q.answer,
                    "shuffled": q.jumbled_answer,
                    "hints":[],
                }
                hints = Hint.objects.filter(question_id=q.question_id)
                # print( 'Hints (%d) : %s' % ( len(hints), ', '.join([h.hint for h in hints])) )
                # print()
                questionsDict[index] = questionDict
                hintsDict[index] = [h.hint for h in hints]

            levelDicts[strLevel] = {
                "released": level.enabled,
                "downloadable": False,
                "enabled": False,
                "questions": questionsDict,
                "hints" : hintsDict,
                "answeredCount" : 0
            }
        output = json.dumps(levelDicts, indent=4)
        return HttpResponse(output, content_type="application/json")

class HintsInLine(admin.StackedInline):
    model = Hint
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('answer', 'thumbnail', 'level', 'enabled')

    fieldsets = [
                 (None, {'fields': ['question_id', 'thumbnail']}),
                 (None, {'fields': ['image', 'level','enabled', 'answer', 'jumbled_answer']}),
    ]
    readonly_fields = ('question_id', 'thumbnail')
    inlines = [HintsInLine]
    class Media:
       js = ('shuffler.js',)