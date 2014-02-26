from django.shortcuts import redirect
from pq.models import Job

from rest_framework import viewsets
from vanilla import CreateView, DetailView

from .jobs import run_check
from .models import Check
from .serializers import JobSerializer


# view to submit form to and redirect to check detail page / then /check/<job>
class JobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'uuid'


# view to show frontpage and form /
class CheckCreateView(CreateView):
    model = Check
    fields = ['requirements']

    def form_valid(self, form):
        check = form.save(commit=False)
        check.job = run_check.delay(form.cleaned_data['requirements'])
        check.save()
        return redirect(check)


class CheckDetailView(DetailView):
    model = Check


# view to fill form with one requirement /requirements/<requirement url>

# view to fill form with one or more projects /<project>
