import logging
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
# from django.forms.models import model_to_dict
from django.http import QueryDict
from .models import Permission, Group, User, UserInfo
from .utils import status_dict
from .forms import PermissionForm, PermissionUpdateForm, PermisssionDeleteForm
from .forms import GroupForm, GroupUpdateForm, GroupDeleteForm, GroupPermissionForm
from .forms import UserForm, UserUpdateForm
from .forms import DeleteForm
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
            if pdata.get("real", "False") == "True":
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
        if not gform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=gform.errors))
        gdata = gform.data.dict()
        try:
            group = Group(name=gdata.get('name'))
            p = Permission.objects.filter(
                name__startswith=gdata.get("permissions", "$"))
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

    def put(self, request):
        gform = GroupUpdateForm(QueryDict(request.body))
        if not gform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=gform.errors))
        gdata = gform.data.dict()
        g = Group.objects.filter(id=gdata.get("id", ""))
        if len(g) == 0:
            message = "Group data with id %s not found" % gdata.get("id")
            return JsonResponse(status_dict(result=False,
                                            message=message))
        g[0].name = gdata.get("name", "")
        try:
            g[0].save()
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("Permission update error: %s", ex)
            return JsonResponse(status_dict(result=False, message=ex.message))

    def delete(self, request):
        pform = GroupDeleteForm(QueryDict(request.body))
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        pdata = pform.data.dict()
        print(pdata)
        try:
            p = Group.objects.filter(id=pdata.get("id"))
            if len(p) == 0:
                message = "Group data not exist!"
                return JsonResponse(status_dict(result=False, message=message))
            if pdata.get("real", "False") == "True":
                p.delete()
            else:
                for d in p:
                    d.is_delete = True
                    d.save()
            message = "Group data with id %s is deleted!" % pdata.get(
                "id")
            return JsonResponse(status_dict(message=message))
        except Exception as ex:
            log.error("Group delete error: %s", ex)
            return JsonResponse(status_dict(result=False, message=ex.message))


class GroupDetailView(View):

    def get(self, request, id):
        try:
            print(id)
            p = Group.objects.filter(id=id, is_delete=False)
            if len(p) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="data not exist!"))
            ret = model_to_dict(p[0], exclude=['is_delete'])
            return JsonResponse(status_dict(data=ret))
        except Exception as ex:
            log.error("get permission error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message=ex.message))


class GroupPermissionView(View):

    def get(self, request, id):
        try:
            p = Group.objects.filter(id=id, is_delete=False)
            if len(p) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="data not exist!"))
            gdata = model_to_dict(p[0], exclude=['is_delete'])
            return JsonResponse(status_dict(data=gdata.get("permission")))
        except Exception as ex:
            log.error("get permission error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="get permission error"))

    def post(self, request, id):
        try:
            p = Group.objects.filter(id=id, is_delete=False)
            if len(p) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="data not exist!"))
            gform = GroupPermissionForm(request.POST)
            if not gform.is_valid():
                return JsonResponse(status_dict(result=False,
                                                message=gform.errors))
            gdata = gform.data.dict()
            permission = Permission.objects.filter(
                name__startswith=gdata.get("name", ""))
            if len(permission) == 0:
                return JsonResponse(status_dict(
                    result=False,
                    message="permission with name %s not exists!" %
                    gdata.get("name", "")))
            for n in permission:
                p[0].permission.add(n)
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("get permission error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="update permission error"))

    def delete(self, request, id):
        p = Group.objects.filter(id=id, is_delete=False)
        print(p)
        if len(p) == 0:
            return JsonResponse(status_dict(result=False,
                                            message="data not exist!"))
        gform = PermisssionDeleteForm(QueryDict(request.body))
        if not gform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=gform.errors))
        gdata = gform.data.dict()
        print(gdata)
        try:
            permission = Permission.objects.filter(id=gdata.get("id", ""))
            if len(permission) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="data not exist!"))
            p[0].permission.remove(permission[0])
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("delete permission error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="delete data error!"))


class UserView(View):

    def get(self, request):
        users = User.objects.filter(is_delete=False)
        data = list(
            [model_to_dict(u, exclude=['is_delete', 'password'])
             for u in users])
        return JsonResponse(status_dict(data))

    def post(self, request):
        uform = UserForm(request.POST)
        if not uform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=uform.errors))
        try:
            udata = uform.data.dict()
            print(udata)
            user = User(**udata)
            userinfo = UserInfo()
            userinfo.save()
            user.user_info = userinfo
            user.save()
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("create user error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="Create user failed!"))


class UserDetailView(View):

    def get(self, request, id):
        try:
            user = User.objects.filter(id=id, is_delete=False)
            if len(user) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="user not exists!"))
            data = model_to_dict(user[0], exclude=['is_delete', 'password'])
            return JsonResponse(status_dict(data))
        except Exception as ex:
            log.error("get user detail error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="get user detail error!"))

    def put(self, request, id):
        user = User.objects.filter(id=id, is_delete=False)
        if len(user) == 0:
            return JsonResponse(status_dict(result=False,
                                            message="user not exists!"))
        uform = UserUpdateForm(QueryDict(request.body))
        if not uform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=uform.errors))
        udata = uform.data.dict()
        print(udata)
        try:
            u = user[0]
            if "password" in udata:
                u.password = udata.get("password")
            if "email" in udata:
                u.email = udata.get("email")
            u.save()
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("update user error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="Update user error!"))

    def delete(self, request, id):
        user = User.objects.filter(id=id, is_delete=False)
        if len(user) == 0:
            return JsonResponse(status_dict(result=False,
                                            message="user not exists!"))
        uform = DeleteForm(QueryDict(request.body))
        if not uform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=uform.errors))
        if uform.data.dict().get("real") == "True":
            user[0].delete()
        else:
            user[0].is_delete = True
            user[0].save()
        return JsonResponse(status_dict())


class UserPermissionView(View):

    def get(self, request, id):
        try:
            u = User.objects.filter(id=id, is_delete=False)
            if len(u) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="data not exist!"))
            udata = model_to_dict(u[0], exclude=['is_delete'])
            return JsonResponse(status_dict(data=udata.get("permission")))
        except Exception as ex:
            log.error("get permission error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="get permission error"))

    def post(self, request, id):
        u = User.objects.filter(id=id, is_delete=False)
        if len(u) == 0:
            return JsonResponse(status_dict(result=False,
                                            message="data not exist!"))
        pform = GroupPermissionForm(request.POST)
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        pdata = pform.data.dict()
        permission = Permission.objects.filter(
            name__startswith=pdata.get("name", ""))
        if len(permission) == 0:
            return JsonResponse(status_dict(
                result=False,
                message="permission with name %s not exists!" %
                pdata.get("name", "")))
        for n in permission:
            u[0].permission.add(n)
        return JsonResponse(status_dict())

    def delete(self, request, id):
        u = User.objects.filter(id=id, is_delete=False)
        if len(u) == 0:
            return JsonResponse(status_dict(result=False,
                                            message="data not exist!"))
        pform = GroupPermissionForm(QueryDict(request.body))
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        pdata = pform.data.dict()
        permission = Permission.objects.filter(
            name__startswith=pdata.get("name", ""))
        if len(permission) == 0:
            return JsonResponse(status_dict(
                result=False,
                message="permission with name %s not exists!" %
                pdata.get("name", "")))
        for n in permission:
            u[0].permission.remove(n)
        return JsonResponse(status_dict())


class UserGroupView(View):
    pass

class UserInfoView(View):
    pass
