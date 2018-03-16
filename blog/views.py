import logging

from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Article, Permission
from .utils import status_dict
from .forms import PermissionForm, PermissionUpdateForm
log = logging.getLogger(__name__)
# Create your views here.


class PermissionView(View):
    def get(self, request):
        permissions = Permission.objects.filter(is_delete=False)
        data = list([model_to_dict(p) for p in permissions])
        ret = status_dict(data)
        return JsonResponse(ret)

    def post(self, request):
        pform = PermissionForm(request.POST)
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors.as_json))
        p = Permission(pform)
        p.save()
        return JsonResponse(status_dict(result=True))

    def put(self, request):
        pform = PermissionUpdateForm(request.POST)
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors.as_json))
        pdata = pform.data
        p = Permission.objects.filter(id=pdata.get("id"))
        if len(p) == 0:
            message = "Permission data with id %s not found" % pdata.get("id")
            return JsonResponse(status_dict(result=False,
                                            message=message))
        p[0].name = pdata.get("name", "")
        try:
            p[0].save()
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("Permission update error: %s", ex)
            return JsonResponse(status_dict(result=False, message=ex.message))


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
