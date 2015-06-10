from django.http import HttpResponse
from .models import Portal, Category, News
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .forms import EnrollementForm
from .models.enrollment import CharacterAttribute, Game
# Create your views here.

def index(request, portal_name):
    portal = get_object_or_404(Portal, name=portal_name)
    return render(request, "SuperPortal/index.html", context={'portal': portal})
    # form = EnrollementForm()
    #
    # choice_field_name = CharacterAttribute.objects.filter(for_game=Game.objects.filter(name="Guild Wars 2"))
    #
    # distinct = CharacterAttribute.objects.filter(for_game=Game.objects.filter(name="Guild Wars 2")).distinct('attribute_name')
    #
    # choices = {}
    #
    # for d in distinct:
    #     choices[d.attribute_name] = CharacterAttribute.objects.filter(for_game=Game.objects.filter(name="Guild Wars 2"), attribute_name=d.attribute_name)
    # return render(request, 'index.html', {'form': form, "choice_field_name": choice_field_name, "distinct":choices})


# class Index(TemplateView):
#     template_name = 'index.html'
#
#     def get(self, request, *args, **kwargs):



def news_detail(request, portal_name, category, news_name):
    portal = Portal.objects.get(name=portal_name)
    news = News.objects.get(category__name=category, title=news_name)
    news.view += 1
    news.save()
    return render(request, 'Portal/News/index.html', {'news' : news})
