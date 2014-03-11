import tempfile
from django import forms

from .models import Check

placeholder = "Project name(s) or URL(s) of pip requirements file"


def filter_requirements(requirements):
    requirements = [requirement.strip() for requirement in requirements]
    return list(filter(None, requirements))


class CheckForm(forms.ModelForm):
    requirements = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'placeholder': placeholder}))

    def clean_requirements(self):
        requirements = self.cleaned_data['requirements']
        # if it's potentially the content of a requirements file
        # we write it to a temporary file and return that as a file:// URL
        if '\n' in requirements or '\r' in requirements:
            split_requirements = filter_requirements(requirements.splitlines())
            line_number = len(split_requirements)
            if line_number > 1:
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(bytes(requirements, 'UTF-8'))
                return ['file://' + tmp.name]
            elif line_number == 1:
                # if someone accidentally added empty lines to a space seprated
                return split_requirements[0]

        # assume the requirements is comma, semicolon or space separated text
        if ',' in requirements:
            requirements = requirements.split(',')
        elif ';' in requirements:
            requirements = requirements.split(';')
        else:
            requirements = requirements.split()
        return filter_requirements(requirements)

    class Meta:
        model = Check
        fields = ['requirements']
