from django.conf import settings


def less_compilation(request):
    return {'compile_less': settings.COMPILE_LESS}
