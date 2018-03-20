import logging
from django.http import JsonResponse
from django.http import QueryDict
from django.views import View
from .utils import model_to_dict, status_dict
from .forms import DeleteForm
log = logging.getLogger(__name__)


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

    def get_filter_dict(self, data):
        return dict(
            {key + '__startswith': value for key, value in data.items()})

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
            filter_dict = self.get_filter_dict(data)
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
            filter_dict = self.get_filter_dict(data)
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
