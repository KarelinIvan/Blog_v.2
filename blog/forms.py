from django import forms


class EmailPostForm(forms.Form):
    """ Класс для валидации данных формы отправки поста по e-mail"""
    name = forms.CharField(max_length=25, help_text='Введите свое имя')
    email = forms.EmailField(help_text='e-mail отправителя')
    to = forms.EmailField(help_text='e-mail получателя')
    comments = forms.CharField(required=False, widget=forms.Textarea, help_text='Комментарии к посту')
