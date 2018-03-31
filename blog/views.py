import logging
from django.http import JsonResponse

from utils.views import ModelViewBase, ModelDetailViewBase
from utils.views import ModelManyToManyViewBase
from utils.utils import status_dict, model_to_dict

from .models import Tags
from .models import Category
from .models import Article, Likes
from blogauth.models import User
from .forms import TagsForm, TagsDetailForm
from .forms import CategoryForm, CategoryDetailForm
from .forms import ArticleForm, ArticleDetailForm, ArticleUserForm
log = logging.getLogger(__name__)


class TagsView(ModelViewBase):
    model = Tags
    form = TagsForm
    exclude = ['is_delete']


class TagsDetailView(ModelDetailViewBase):
    model = Tags
    form = TagsDetailForm
    exclude = ['is_delete']


class CategoryView(ModelViewBase):
    model = Category
    form = CategoryForm
    exclude = ['is_delete']


class CategoryDetailView(ModelDetailViewBase):
    model = Category
    form = CategoryDetailForm
    exclude = ['is_delete']


class ArticleView(ModelViewBase):
    model = Article
    form = ArticleForm
    exclude = ['is_delete', 'content', 'author', 'category']

    def get(self, request):
        if self.model is None:
            raise NotImplementedError("Method not implemented!")
        querys = self.model.objects.filter(is_delete=False)
        data = []
        for q in querys:
            tmp = model_to_dict(q, fields=self.fields, exclude=self.exclude)
            tmp['author'] = q.author.username
            tmp['category'] = q.category.name
            tmp['likes'] = model_to_dict(q.likes,
                                         fields=['id', 'username',
                                                 'readers', 'like',
                                                 'disagree'])
            data.append(tmp)
        return JsonResponse(status_dict(data))

    def post(self, request):
        aform = self.form(request.POST)
        if not aform.is_valid():
            return JsonResponse(status_dict(result=False,
                                            message=aform.errors))
        try:
            adata = aform.data.dict()
            authors = User.objects.filter(id=adata.pop("author"),
                                          is_delete=False)
            if len(authors) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="author not exists!"))
            adata['author'] = authors[0]
            categorys = Category.objects.filter(id=adata.pop("category"),
                                                is_delete=False)
            if len(categorys) == 0:
                return JsonResponse(status_dict(result=False,
                                                message="category not exists"))
            adata['category'] = categorys[0]
            article = self.model(**adata)
            likes = Likes()
            likes.save()
            article.likes = likes
            article.save()
            return JsonResponse(status_dict(model_to_dict(article)))
        except Exception as ex:
            log.error("create user error: %s", ex)
            return JsonResponse(status_dict(result=False,
                                            message="Create user failed!"))


class ArticleDetailView(ModelDetailViewBase):
    model = Article
    form = ArticleDetailForm
    fields = []
    exclude = ['is_delete', 'author', 'category']

    def get(self, request, id):
        article = self.get_query(id)
        if article is None:
            return JsonResponse(status_dict(result=False,
                                            message="Data not exists!"))
        article.likes.readers += 1
        article.likes.save()
        data = model_to_dict(article, fields=self.fields, exclude=self.exclude)
        data['author'] = article.author.username
        data['category'] = article.category.name
        data['likes'] = model_to_dict(article.likes,
                                      fields=['id', 'username',
                                              'readers', 'like',
                                              'disagree'])

        return JsonResponse(status_dict(data))


class ArticleLikeView(ModelManyToManyViewBase):
    model = Article
    form = ArticleUserForm
    many_to_many_model = User
    many_to_many_name = "like"
    opposite_name = "disagree"
    # exclude = ['is_delete']
    fields = ['id', 'username', 'like']

    def get_query(self, id):
        if self.model is None:
            raise NotImplementedError("Method not implemented!")
        querys = self.model.objects.filter(id=id, is_delete=False)
        if len(querys) == 0:
            return None
        else:
            return querys[0].likes

    def get_filter_dict(self, data):
        return data

    def add_or_remove(self, model, many_model, method="add"):
        many_list = getattr(model, self.many_to_many_name)
        disagree_list = getattr(model, self.opposite_name)
        for m in many_model:
            if method == "add":
                if m in disagree_list.iterator():
                    disagree_list.remove(m)
                many_list.add(m)
            elif method == "delete":
                many_list.remove(m)
        model.save()


class ArticleDisagreeView(ArticleLikeView):
    many_to_many_name = "disagree"
    opposite_name = "like"
    fields = ['id', 'username', 'disagree']


class ArticleTagsView(ModelManyToManyViewBase):
    model = Article
    many_to_many_name = "tags"
    many_to_many_model = Tags
    form = TagsDetailForm
    fields = ['id', 'name', 'tags']

    def get_filter_dict(self, data):
        return data
