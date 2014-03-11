from django.shortcuts import redirect

from rest_framework import viewsets
from vanilla import CreateView

from .forms import CheckForm
from .jobs import run_check, get_compatible, get_total
from .models import Check
from .serializers import CheckSerializer


class CheckViewSet(viewsets.mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    lookup_field = 'pk'
    template_name = 'checks/check_detail.html'


class CheckCreateView(CreateView):
    form_class = CheckForm
    model = Check

    def form_valid(self, form):
        check = form.save()
        run_check.delay(check.pk)
        return redirect(check)

    def get_context_data(self, *args, **kwargs):
        context = super(CheckCreateView, self).get_context_data(*args,
                                                                **kwargs)
        context.update({
            'compatible': get_compatible(),
            'total': get_total(),
        })
        return context
