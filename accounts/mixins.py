from django.shortcuts import redirect


class AssertNotLoggedInMixin:
    redirect_url = None

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url or self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

