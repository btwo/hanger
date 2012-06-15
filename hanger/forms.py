#!/usr/bin/env python2.7
# coding=utf-8
'''
WTForm with tornado.
'''
import wtforms

from wtforms import TextField
from wtforms import IntegerField as _IntegerField
from wtforms import DecimalField as _DecimalField
from wtforms import DateField as _DateField
from wtforms.widgets import Input

class FormsDict(dict):
    '''WTForms form object dict.'''
    def append(self, Form):
        self[Form.__name__] = Form()


class AutoFormsMixin(object):
    '''Auto add form to `forms`dict in the templates.'''
    Form = None
    formset = []

    def __init__(self, *args, **kwargs):
        self.forms = FormsDict()
        if self.Form:
            self.forms.append(self.Form)
        for Form in self.formset:
            self.forms.append(Form)
        super(AutoFormsMixin, self).__init__(*args, **kwargs)

    def form_loader(self, key=None, validate=True):
        '''Get and validate a form.'''
        if not key:
            # return default form
            try:
                form = self.Form(self)
            except TypeError:
                raise RuntimeError("Not set default form.")
        else:
            form = self.forms[key].__class__(self)
        if validate:
            if not self.form_validate(form):
                # form validate.
                raise RuntimeError("form is not pass the validation.")
        return form

    def form_validate(self, form, *args, **kwargs):
        '''Automated handle of Forms validate.'''
        if form.validate():
            return form
        self.forms.update({form.__class__.__name__: form})
        self.render(*args, **kwargs)
        return False

    def render(self, template_name = "", **context):
        if not template_name:
            template_name = self.template_name
        super(AutoFormsMixin, self).render(
            template_name=template_name, forms=self.forms, **context)


class FormDict(dict):
    '''Tornado handler arguments to MultiDict, wtforms required.'''
    def __init__(self, arguments):
        self.arguments = arguments

    def __iter__(self):
        return iter(self.arguments)

    def __len__(self):
        return len(self.arguments)

    def __contains__(self, name):
        return (name in self.arguments)

    def getlist(self, key):
        """
        Returns the list of values for the passed key. If key doesn't exist,
        then an empty list is returned.
        """
        try:
            return self.arguments[key]
        except KeyError:
            return []


class Form(wtforms.Form):
    '''
    Base form class
    '''
    def __init__(self, handler = None, obj=None, prefix='', formdata=None,
                 **kwargs):
        if handler:
            formdata = FormDict(handler.request.arguments)
            self.handler = handler
            self.current_user = handler.current_user
        super(Form, self).__init__(formdata = formdata, **kwargs)


#some html5 field
#form https://github.com/rduplain/flask-wtf/
class DateInput(Input):
    """
    Creates `<input type=date>` widget
    """
    input_type = "date"


class NumberInput(Input):
    """
    Creates `<input type=number>` widget
    """
    input_type="number"


class RangeInput(Input):
    """
    Creates `<input type=range>` widget
    """
    input_type="range"


class URLInput(Input):
    """
    Creates `<input type=url>` widget
    """
    input_type = "url"


class EmailInput(Input):
    """
    Creates `<input type=email>` widget
    """

    input_type = "email"


class SearchInput(Input):
    """
    Creates `<input type=search>` widget
    """

    input_type = "search"

class TelInput(Input):
    """
    Creates `<input type=tel>` widget
    """

    input_type = "tel"


class SearchField(TextField):
    """
    **TextField** using **SearchInput** by default
    """
    widget = SearchInput()


class DateField(_DateField):
    """
    **DateField** using **DateInput** by default
    """
 
    widget = DateInput()


class URLField(TextField):
    """
    **TextField** using **URLInput** by default
    """
 
    widget = URLInput()
    

class EmailField(TextField):
    """
    **TextField** using **EmailInput** by default
    """
 
    widget = EmailInput()

class TelField(TextField):
    """
    **TextField** using **TelInput** by default
    """

    widget = TelInput()


class IntegerField(_IntegerField):
    """
    **IntegerField** using **NumberInput** by default
    """

    widget = NumberInput()


class DecimalField(_DecimalField):
    """
    **DecimalField** using **NumberInput** by default
    """

    widget = NumberInput()


class IntegerRangeField(_IntegerField):
    """
    **IntegerField** using **RangeInput** by default
    """

    widget = RangeInput()


class DecimalRangeField(_DecimalField):
    """
    **DecimalField** using **RangeInput** by default
    """

    widget = RangeInput()
