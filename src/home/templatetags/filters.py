from django import template
from users.models import User
register = template.Library()


@register.filter(name='order_by_merge_sort')
def order_by_merge_sort(value, ordering):
    result = filter(lambda x:x if x['category__name'] == ordering else None, value)
    print(ordering)
    return result


# @register.filter(name='build_absolute_url')
# def build_absolute_url(value, request):
#     scheme = request.headers.get('X-Forwarded-Proto')
#     host = request.headers.get('host')

#     if '/media/' in value:
#         url = f'{scheme}://{host}{value}'
#     else:
#         url = f'{scheme}://{host}/media/{value}'
#     return url