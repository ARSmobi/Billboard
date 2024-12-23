from django.http import Http404


class AuthorRequiredMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user == obj.user:
            raise Http404('У вас нет доступа к этой странице.')
        return obj
