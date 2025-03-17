from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'content', 'image']
        widgets = {
            # Ustawiamy widget textarea z unikalnym id, które wykorzystamy przez Quill
            'content': forms.Textarea(attrs={'id': 'quill-editor'})
        }
