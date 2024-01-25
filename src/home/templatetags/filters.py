from django import template
from users.models import User
register = template.Library()

@register.filter(name='order_by_merge_sort')
def order_by_merge_sort(value, ordering):
    value = list(value)
    length = len(value)
    if length > 1:
        left_array = value[: length // 2]
        right_array = value[length // 2 :]
        i = 0
        j = 0
        k = 0
    
        order_by_merge_sort(left_array, ordering)
        order_by_merge_sort(right_array, ordering)

        lLength = len(left_array)
        rLength = len(right_array)

        while i < lLength and j < rLength:
            if left_array[i][ordering] < right_array[j][ordering]:
                value[k] = left_array[i]
                i += 1
            else:
                value[k] = right_array[j]
                j += 1
            k += 1
                

        while i < lLength:
            value[k] = left_array[i]
            k += 1
            i += 1
        
        while j < rLength:
            value[k] = right_array[j]
            k += 1
            j += 1
    return value

@register.filter(name='order_by_merge_sort_descending')
def order_by_merge_sort_descending(value, ordering):
    value = list(value)
    length = len(value)
    if length > 1:
        left_array = value[: length // 2]
        right_array = value[length // 2 :]
        i = 0
        j = 0
        k = 0
    
        order_by_merge_sort_descending(left_array, ordering)
        order_by_merge_sort_descending(right_array, ordering)

        lLength = len(left_array)
        rLength = len(right_array)

        while i < lLength and j < rLength:
            if left_array[i][ordering] > right_array[j][ordering]:
                value[k] = left_array[i]
                i += 1
            else:
                value[k] = right_array[j]
                j += 1
            k += 1
                

        while i < lLength:
            value[k] = left_array[i]
            k += 1
            i += 1
        
        while j < rLength:
            value[k] = right_array[j]
            k += 1
            j += 1
    return value


@register.filter(name='filter_by_category')
def filter_by_category_name(value, ordering):
    result = filter(lambda x:x if x['category__slug'] == ordering else None, value)
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