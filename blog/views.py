import logging

from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Article, Permission
from .utils import status_dict

log = logging.getLogger(__name__)
# Create your views here.

class ArticleView(View):
    def get(self, request):
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 5)
        articles = Article.objects.all()
        paginator = Paginator(articles, page_size)
        try:
            data = serialize('json', paginator.page(int(page)))
            options = {
                "page": page,
                "page_total": paginator.num_pages,
                "total": paginator.count,
            }
            ret = status_dict(data, **options)
            return JsonResponse(ret)
        except Exception as ex:
            log.error("get article error: %s", ex)
            return JsonResponse(status_dict(message=ex.message))

    def post(self, request):
        title = request.POST.get("title")
        author = request.POST.get("author")
        category = request.POST.get("category")
        tags = request.POST.get("tags")
        abstract = request.POST.get("")



class PermissionView(View):
    def get(self, request):
        permissions = Permission.objects.filter(is_delete=False)
        data = list([model_to_dict(p) for p in permissions])
        ret = status_dict(data)
        return JsonResponse(ret)
