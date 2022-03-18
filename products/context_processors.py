from .forms import ProductSearchForm


def header_form(request):
    return {'search_form': ProductSearchForm()}
