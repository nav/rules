from django.contrib import admin
from api.rules.models import Rule, RuleSet


class RuleSetAdmin(admin.ModelAdmin):
    pass


admin.site.register(RuleSet, RuleSetAdmin)
admin.site.register(Rule)
