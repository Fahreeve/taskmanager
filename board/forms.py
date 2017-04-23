from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import BoundField
from django.forms.utils import ErrorList
from django.utils.encoding import force_text
from django.utils.html import format_html, format_html_join

from board.models import Task, Comment


class MyBoundField(BoundField):
    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        attrs['class'] = 'form-control'
        return super().as_widget(widget, attrs, only_initial)


class MyErrorList(ErrorList):
    def __str__(self):
        if not self.data:
            return ''

        return format_html(
            '{}',
            format_html_join('', '<p class="text-danger">{}</p>', ((force_text(e),) for e in self))
        )


class MyFormMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = MyErrorList

    def __getitem__(self, name):
        "Returns a BoundField with the given name."
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError(
                "Key '%s' not found in '%s'. Choices are: %s." % (
                    name,
                    self.__class__.__name__,
                    ', '.join(sorted(f for f in self.fields)),
                )
            )
        if name not in self._bound_fields_cache:
            self._bound_fields_cache[name] = MyBoundField(self, field, name)
        return self._bound_fields_cache[name]

    def __str__(self):
        return self._html_output(
                normal_row='<div class="form-group" %(html_class_attr)s>%(label)s %(field)s%(errors)s%(help_text)s</div>',
                error_row='<p class="text-danger">%s</p>',
                row_ender='</div>',
                help_text_html=' <span class="helptext">%s</span>',
                errors_on_separate_row=False)


class MyAuthenticationForm(MyFormMixin, AuthenticationForm):
    pass


class ChangeTaskForm(MyFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'disabled': True}),
            'status': forms.Select(attrs={'onchange': 'enableDeadlineField(this.selectedIndex);'})
        }


class AddCommentForm(MyFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2})
        }

    def save(self, commit=True):
        self.instance.creator = self.initial['creator']
        self.instance.task = self.initial['task']
        return super().save(commit)
