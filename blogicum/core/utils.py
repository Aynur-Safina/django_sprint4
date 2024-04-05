from blogicum.const import PUBL_COUNT
from django.core.paginator import Paginator


def get_page_obj(request, paginated_obj):
    """Пагинация по 10 публикаций на странице."""
    paginator = Paginator(paginated_obj, PUBL_COUNT)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
