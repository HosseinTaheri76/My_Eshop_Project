from .models import SiteInfo


def site_info(request):
    return {'site_info': SiteInfo.load()}
