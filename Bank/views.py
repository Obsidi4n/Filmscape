from django.shortcuts import render

from .models import Level, Question, Hint


def LevelGenerator(request):
    level_list = Level.objects.all()
    context = {
                'level_list': level_list,
        }
    return render(request, 'admin/levelGenerator/levelGenerator.html', context)