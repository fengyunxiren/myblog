import logging
from django.views import View
from django.http import JsonResponse
from django.http import QueryDict
from .models import Permission, Group, User, UserInfo
from .utils import status_dict
from .forms import PermissionForm, PermissionDetailForm
from .forms import GroupForm, GroupDetailForm
from .forms import UserForm
from .forms import DeleteForm
from .utils import model_to_dict

log = logging.getLogger(__name__)
# Create your views here.


class ModelViewBase(View):
    model = None
    form = None
    fields = []
    exclude = []

    def get(self, request):
        if self.model is None:
            raise NotImplementedError("Method not implemented!")
        querys = self.model.objects.filter(is_delete=False)
        data = list(
            [model_to_dict(q, fields=self.fields, exclude=self.exclude)
             for q in querys])
        return JsonResponse(status_dict(data))

    def post(self, request):
        if self.form is None:
            raise NotImplementedError("Method not implemented!")
        pform = self.form(request.POST)
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        try:
            pform.save()
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("Create data error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="Create data error!"))


class ModelDetailViewBase(View):
    model = None
    form = None
    deleteform = DeleteForm
    fields = []
    exclude = []

    def get_query(self, id):
        if self.model is None:
            raise NotImplementedError("Method not implemented!")
        querys = self.model.objects.filter(id=id, is_delete=False)
        if len(querys) == 0:
            return None
        else:
            return querys[0]

    def get(self, request, id):
        q = self.get_query(id)
        if q is None:
            return JsonResponse(status_dict(result=False,
                                            message="Data not Found!"))
        data = model_to_dict(
            q, fields=self.fields, exclude=self.exclude)
        return JsonResponse(status_dict(data))

    def put(self, request, id):
        if self.form is None:
            raise NotImplementedError("Method not implemented!")
        q = self.get_query(id)
        if q is None:
            return JsonResponse(status_dict(result=False,
                                            message="Data not Found!"))
        pform = self.form(QueryDict(request.body))
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        data = pform.data.dict()
        try:
            for key, value in data.items():
                setattr(q, key, value)
            q.save()
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("Update data error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="Update data error!"))

    def delete(self, request, id):
        q = self.get_query(id)
        if q is None:
            return JsonResponse(status_dict(result=False,
                                            message="Data not Found!"))
        dform = self.deleteform(QueryDict(request.body))
        if not dform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=dform.errors))
        real = dform.data.dict().get('real', "False")
        if real == "False":
            q.is_delete = True
            q.save()
        else:
            q.delete()
        return JsonResponse(status_dict())


class ModelManyToManyViewBase(ModelDetailViewBase):
    many_to_many_model = None
    many_to_many_name = None

    def get(self, request, id):
        if self.many_to_many_name is None:
            raise NotImplementedError("Method not implemented!")
        q = self.get_query(id)
        if q is None:
            return JsonResponse(status_dict(result=False,
                                            message="Data not Found!"))
        data = model_to_dict(q, fields=self.fields, exclude=self.exclude)
        return JsonResponse(status_dict(data.get(self.many_to_many_name)))

    def put(self, request, id):
        if self.many_to_many_model is None or self.form is None or \
           self.many_to_many_name is None:
            raise NotImplementedError("Method not implemented!")
        q = self.get_query(id)
        if q is None:
            return JsonResponse(status_dict(result=False,
                                            message="Data not Found!"))

        pform = self.form(QueryDict(request.body))
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        data = pform.data.dict()
        try:
            filter_dict = dict(
                {key + '__startswith': value for key, value in data.items()})
            filter_dict['is_delete'] = False
            mquerys = self.many_to_many_model.objects.filter(**filter_dict)
            many_list = getattr(q, self.many_to_many_name)
            for m in mquerys:
                many_list.add(m)
            q.save()
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("Update data error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="Update data error!"))

    def delete(self, request, id):
        if self.many_to_many_model is None or self.form is None or \
           self.many_to_many_name is None:
            raise NotImplementedError("Method not implemented!")
        q = self.get_query(id)
        if q is None:
            return JsonResponse(status_dict(result=False,
                                            message="Data not Found!"))

        pform = self.form(QueryDict(request.body))
        if not pform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=pform.errors))
        data = pform.data.dict()
        try:
            filter_dict = dict(
                {key + '__startswith': value for key, value in data.items()})
            filter_dict['is_delete'] = False
            mquerys = self.many_to_many_model.objects.filter(**filter_dict)
            many_list = getattr(q, self.many_to_many_name)
            for m in mquerys:
                many_list.remove(m)
            q.save()
            return JsonResponse(status_dict())
        except Exception as ex:
            log.error("Delete data error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="Delete data error!"))


class PermissionView(ModelViewBase):
    model = Permission
    form = PermissionForm
    exclude = ['is_delete']


class PermissionDetailView(ModelDetailViewBase):
    model = Permission
    form = PermissionDetailForm
    exclude = ['is_delete']


class GroupView(ModelViewBase):
    model = Group
    form = GroupForm
    exclude = ['is_delete']


class GroupDetailView(ModelDetailViewBase):
    model = Group
    form = GroupDetailForm
    exclude = ['is_delete']


class GroupPermissionView(ModelManyToManyViewBase):
    model = Group
    many_to_many_model = Permission
    many_to_many_name = "permission"
    form = PermissionDetailForm
    exclude = ['is_delete']


class UserView(ModelViewBase):
    model = User
    form = UserForm
    exclude = ['is_delete']

    # def get(self, request):
    #     users = User.objects.filter(is_delete=False)
    #     data = list(
    #         [model_to_dict(u, exclude=['is_delete', 'password'])
    #          for u in users])
    #     return JsonResponse(status_dict(data))

    # def post(self, request):
    #     uform = UserForm(request.POST)
    #     if not uform.is_valid():
    #         return JsonResponse(status_dict(result=False,
    #                                         message=uform.errors))
    #     try:
    #         udata = uform.data.dict()
    #         print(udata)
    #         user = User(**udata)
    #         userinfo = UserInfo()
    #         userinfo.save()
    #         user.user_info = userinfo
    #         user.save()
    #         return JsonResponse(status_dict())
    #     except Exception as ex:
    #         log.error("create user error: %s", ex)
    #         return JsonResponse(status_dict(result=False,
    #                                         message="Create user failed!"))


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
