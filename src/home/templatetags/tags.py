from django import template
register = template.Library()





@register.simple_tag(name='filter_by_category')
def build_absolute_url(request, path):
    scheme = request.headers.get('X-Forwarded-Proto')
    host = request.headers.get('host')

    if '/media/' in path:
        url = f'{scheme}://{host}{path}'
    else:
        url = f'{scheme}://{host}/media/{path}'
    return url