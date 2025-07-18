from django import forms
from .models import Comment, Post
from ckeditor.widgets import CKEditorWidget


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                    'placeholder': 'Your name'}))
    email = forms.EmailField(widget=forms.EmailInput(
                                    attrs={'class': 'form-control',
                                    'placeholder': 'Your email address here'}))
    to = forms.EmailField(widget=forms.EmailInput(
                                    attrs={'class': 'form-control',
                                    'placeholder': "Receiver's email address"}))
    comments = forms.CharField(required=False, widget=forms.Textarea(
                                    attrs={'class': 'form-control',
                                    'placeholder': 'Write message here'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

        # You either use this method or use the custom tags and filter method to specify attrs
        #  widgets = {
        #     'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
        #     'body': Textarea(attrs={'class': 'form-control', 'placeholder': 'Text'}),
        # }
        

class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'        