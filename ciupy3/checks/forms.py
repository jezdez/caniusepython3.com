import pkg_resources
from pip.vcs import vcs
from django import forms
from .models import Check

placeholder = "Project name(s) or URL(s) of pip requirements file"


def parse_requirement(project_name):
    try:
        req = pkg_resources.Requirement.parse(project_name)
    except ValueError:
        return project_name
    else:
        return req.project_name


def is_vcs_requirement(requirement):
    full_scheme = tuple(['%s://' % scheme
                         for scheme in vcs.all_schemes])
    return not requirement.startswith(full_scheme)


def filter_requirements(requirements):
    requirements = [parse_requirement(requirement.strip())
                    for requirement in requirements]
    return list(filter(is_vcs_requirement, filter(None, requirements)))


def split_requirements(requirements):
    if ',' in requirements:
        return requirements.split(',')
    elif ';' in requirements:
        return requirements.split(';')
    else:
        return requirements.split()


class CheckForm(forms.ModelForm):
    requirements = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'placeholder': placeholder}))

    def clean_requirements(self):
        requirements = self.cleaned_data['requirements']
        # if it's potentially the content of a requirements file
        # we write it to a temporary file and return that as a file:// URL
        splitlines = filter_requirements(requirements.splitlines())
        if len(splitlines) > 1:
            requirements = []
            for splitline in splitlines:
                if splitline.startswith(('#', '-')):
                    continue
                requirements.extend(split_requirements(splitline))
        else:
            # assume the requirements is comma, semicolon or space separated text
            requirements = split_requirements(splitlines[0])
        return filter_requirements(requirements)

    class Meta:
        model = Check
        fields = ['requirements']
