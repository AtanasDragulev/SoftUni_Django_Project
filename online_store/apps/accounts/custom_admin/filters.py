from django.contrib.auth.models import Group
from django.contrib.admin import SimpleListFilter


class GroupFilter(SimpleListFilter):
    title = 'Groups'
    parameter_name = 'groups'

    def lookups(self, request, model_admin):
        group_names = Group.objects.values_list('name', flat=True)
        return [(group_name, group_name) for group_name in group_names]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(groups__name=self.value())
        return queryset
