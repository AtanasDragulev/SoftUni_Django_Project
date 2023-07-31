from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ImproperlyConfigured

from django.utils.decorators import method_decorator
from django.views import View


class AccessRequiredMixin(View):
    REQUIRED_GROUP = "Admins"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.REQUIRED_GROUP:
            raise ImproperlyConfigured(
                "The required_group attribute must be set on the view.")

        if not request.user.groups.filter(name=self.REQUIRED_GROUP).exists():
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


def group_required(group_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:

                raise PermissionDenied

        return wrapper

    return decorator
