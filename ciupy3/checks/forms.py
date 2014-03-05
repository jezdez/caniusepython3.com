from django import forms

from .models import Check


class CheckForm(forms.ModelForm):
    requirements = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Project(s) or requirements URL(s)'}))

    def clean_requirements(self):
        requirements = self.cleaned_data['requirements']
        if ',' in requirements:
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
