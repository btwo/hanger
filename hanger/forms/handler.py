#!/usr/bin/env python2.7
# coding=utf-8
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
