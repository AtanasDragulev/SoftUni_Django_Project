from django.views.decorators.cache import cache_control
from online_store.apps.core.models import Category
from .forms import SearchForm


def sidebar_categories(request):
    main_categories = Category.objects.filter(parent_category=None)
    categories = []

    for main_category in main_categories:
        sub_categories = main_category.category_set.all().order_by('order')
        categories.append({'main_category': main_category, 'sub_categories': sub_categories})

    return {'sidebar_categories': categories}


def search_form(request):
    form = SearchForm(request.POST)
    return {'search_form': form}
