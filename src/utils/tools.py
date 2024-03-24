from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_paginator(request, obj, count):
    if obj:
        paginator = Paginator(obj, count)
        page = request.GET.get('page')
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
                obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)
    else:
        paginator = None
    return (obj, paginator)