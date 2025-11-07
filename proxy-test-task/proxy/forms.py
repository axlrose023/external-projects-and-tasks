from django import forms

from .models import UserSite


class UserSiteForm(forms.ModelForm):
    class Meta:
        model = UserSite
        fields = ['name', 'url']

    def __init__(self, *args, **kwargs):
        super(UserSiteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control col-4'})
            if field_name == 'url':
                field.widget.attrs.update({'placeholder': 'start with https://'})
