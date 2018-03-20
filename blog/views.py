import logging

from utils.views import ModelViewBase, ModelDetailViewBase
from utils.views import ModelManyToManyViewBase
from utils.utils import status_dict

from .models import Tags
from .models import Category
from .forms import TagsForm, TagsDetailForm
from .forms import CategoryForm, CategoryDetailForm
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


class CategoryDetailView(CategoryDetailForm):
    model = Category
    form = CategoryDetailForm
    exclude = ['is_delete']