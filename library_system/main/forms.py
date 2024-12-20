from django import forms
from .models import Book, Genre, Comment
from django.forms import ModelForm

class BookForm(ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        label='Жанры',
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'description', 'genres', 'published_date', 'image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название книги*',
                'required': 'required',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор книги*',
                'required': 'required',
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Издатель',
                'required': 'required',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание*',
                'required': 'required',
                'rows': 3,
            }),
            'published_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Дата издания*',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update

    def as_div(self):
        return self._html_output(
            normal_row='<div class="styled-field " id="%(html_name)s">%(label)s %(field)s%(help_text)s</div>',
            row_ender='</div>',
            errors_on_separate_row=True,
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Комментарий'
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class BookFormEdit(ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        label='Жанры',
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'description', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название книги*',
                'required': 'required',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор книги*',
                'required': 'required',
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Издатель',
                'required': 'required',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание*',
                'required': 'required',
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        super(BookFormEdit, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update

    def as_div(self):
        return self._html_output(
            normal_row='<div class="styled-field " id="%(html_name)s">%(label)s %(field)s%(help_text)s</div>',
            row_ender='</div>',
            errors_on_separate_row=True,
        )
