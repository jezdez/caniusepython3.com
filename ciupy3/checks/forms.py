import tempfile
from django import forms

from .models import Check

placeholder = "Project name(s) or URL(s) of pip requirements file"


class CheckForm(forms.ModelForm):
    requirements = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'placeholder': placeholder}))

    def clean_requirements(self):
        requirements = self.cleaned_data['requirements']
        # if it's potentially the content of a requirements file
        # we write it to a temporary file and return that as a file:// URL
        if '\n' in requirements or '\r' in requirements:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_requirements:
                tmp_requirements.write(bytes(requirements, 'UTF-8'))
            requirements = ['file://' + tmp_requirements.name]
        elif ',' in requirements:
            requirements = requirements.split(',')
        elif ';' in requirements:
            requirements = requirements.split(';')
        else:
            requirements = requirements.split()
        requirements = [requirement.strip() for requirement in requirements]
        return list(filter(None, requirements))

    class Meta:
        model = Check
        fields = ['requirements']
