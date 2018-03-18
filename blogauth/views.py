import logging
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
# from django.forms.models import model_to_dict
from django.http import QueryDict
from .models import Permission, Group
from .utils import status_dict
from .forms import PermissionForm, PermissionUpdateForm, PermisssionDeleteForm
from .forms import GroupForm
from .utils import model_to_dict

log = logging.getLogger(__name__)
# Create your views here.


class PermissionView(View):
    def get(self, request):
        permissions = Permission.objects.filter(is_delete=False)
        data = list([model_to_dict(p, exclude=['is_delete'])
                     for p in permissions])
        ret = status_dict(data)
        return JsonResponse(ret)

    def post(self, request):
        pform = PermissionForm(request.POST)
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        pdata = pform.data.dict()
        try:
            p = Permission(**pdata)
            p.save()
            return JsonResponse(status_dict(result=True))
        except Exception as ex:
            log.error("Permission create error: %s", ex)
            return JsonResponse(status_dict(result=False, message=ex.message))

    def put(self, request):
        pform = PermissionUpdateForm(QueryDict(request.body))
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        pdata = pform.data.dict()
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

    def delete(self, request):
        pform = PermisssionDeleteForm(QueryDict(request.body))
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        pdata = pform.data.dict()
        try:
            p = Permission.objects.filter(id=pdata.get("id"))
            if len(p) == 0:
                message = "Permission data not exist!"
                return JsonResponse(status_dict(result=False, message=message))
            if pdata.get("real", False) is True:
                p.delete()
            else:
                for d in p:
                    d.is_delete = True
                    d.save()
            message = "Permission data with id %s is deleted!" % pdata.get(
                "id")
            return JsonResponse(status_dict(message=message))
        except Exception as ex:
            log.error("Permission delete error: %s", ex)
            return JsonResponse(status_dict(result=False, message=ex.message))


class PermissionDetailView(View):
    def get(self, request, id):
        try:
            print(id)
            p = Permission.objects.filter(id=id, is_delete=False)
            if len(p) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="data not exist!"))
            ret = model_to_dict(p[0], exclude=['is_delete'])
            return JsonResponse(status_dict(data=ret))
        except Exception as ex:
            log.error("get permission error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message=ex.message))


class GroupView(View):
    def get(self, request):
        groups = Group.objects.filter(is_delete=False)
        data = list([model_to_dict(g, exclude=['is_delete'])
                     for g in groups])
        ret = status_dict(data)
        return JsonResponse(ret)

    def post(self, request):
        gform = GroupForm(request.POST)
        print(gform.data.dict())
        if not gform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=gform.errors))
        gdata = gform.data.dict()
        print(gdata)
        try:
            group = Group(name=gdata.get('name'))
            p = Permission.objects.filter(id=gdata.get("permission"))
            print(group)
            print(p)
            group.save()
            for pp in p:
                group.permission.add(pp)
            group.save()
            return JsonResponse(status_dict(result=True))
        except Exception as ex:
            log.error("create group error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="create group error!"))
