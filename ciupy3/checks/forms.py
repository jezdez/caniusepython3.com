from django import forms

from .models import Check


class CheckForm(forms.ModelForm):
    requirements = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Project name(s) or '
                              'requirements file URL(s)'}))

    def clean_requirements(self):
        requirements = self.cleaned_data['requirements']
        if ',' in requirements:
            requirements = requirements.split(',')
        elif ';' in requirements:
            requirements = requirements.split(';')
        else:
            requirements = requirements.split()
        return [requirement.strip() for requirement in requirements]

    class Meta:
        model = Check
        fields = ['requirements']
