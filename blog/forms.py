from django import forms

from blog.models import Comment


class EmailPostForm(forms.Form):
    """ Класс для валидации данных формы отправки поста по e-mail"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """ Форма комментариев """

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    """ Форма поиска """
    query = forms.CharField()
