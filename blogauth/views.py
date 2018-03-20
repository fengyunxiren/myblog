import logging
import hashlib
from mysite.settings import SECRET_KEY
from django.http import JsonResponse
from .models import Permission, Group, User, UserInfo
from .forms import PermissionForm, PermissionDetailForm
from .forms import GroupForm, GroupDetailForm
from .forms import UserForm, UserDetailForm, UserInfoDetailForm

from utils.views import ModelViewBase, ModelDetailViewBase
from utils.views import ModelManyToManyViewBase
from utils.utils import status_dict

log = logging.getLogger(__name__)
# Create your views here.


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
    exclude = ['is_delete', 'password', 'user_info', 'group', 'permission']

    def post(self, request):
        uform = self.form(request.POST)
        if not uform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=uform.errors))
        try:
            udata = uform.data.dict()
            udata['password'] = self.password_encrypt(udata.get("password"))
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

    def password_encrypt(self, password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode("utf-8"))
        sha256.update(SECRET_KEY.encode("utf-8"))
        return sha256.hexdigest()


class UserDetailView(ModelDetailViewBase):
    model = User
    form = UserDetailForm
    exclude = ['is_delete', 'password', 'user_info', 'group', 'permission']


class UserPermissionView(ModelManyToManyViewBase):
    model = User
    many_to_many_model = Permission
    many_to_many_name = "permission"
    form = PermissionDetailForm
    exclude = ['is_delete']


class UserGroupView(ModelManyToManyViewBase):
    model = User
    many_to_many_model = Group
    many_to_many_name = "group"
    form = GroupDetailForm
    exclude = ['is_delete']

    def get_filter_dict(self, data):
        return data


class UserInfoView(ModelDetailViewBase):
    model = User
    form = UserInfoDetailForm
    exclude = ['is_delete']

    def get_query(self, id):
        if self.model is None:
            raise NotImplementedError("Method not implemented!")
        querys = self.model.objects.filter(id=id, is_delete=False)
        if len(querys) == 0:
            return None
        else:
            return querys[0].user_info

    def delete(self, request, id):
        return JsonResponse(status_dict(result=False,
                                        message="Can not delete!"))
