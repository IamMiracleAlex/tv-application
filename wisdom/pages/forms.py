from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from pages.models import Quote


class QuoteAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Quote
        fields = '__all__'
