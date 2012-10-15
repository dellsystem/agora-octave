from django.contrib import admin

from apps.snippet.models import Snippet, CodeLanguage


admin.site.register(Snippet)
admin.site.register(CodeLanguage)
