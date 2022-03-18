from django.http import HttpResponseNotFound


def ajax_only(func):
    def wrapper(request, *args, **kwargs):
        if request.is_ajax():
            return func(request, *args, **kwargs)
        return HttpResponseNotFound()
    return wrapper
