import copy
from itertools import chain

from django import forms
from django.core import validators
from django.forms.utils import flatatt
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_str
from django.utils.html import escape
from django.utils.text import capfirst
from django.utils.safestring import mark_safe

class DynamicModelChoiceField(forms.Field):
    def __init__(self, model, *args, **kwargs):
        super(DynamicModelChoiceField, self).__init__(*args, **kwargs)
        self.model = model
        widget_kwargs = {}
        if 'display_template' in kwargs:
            widget_kwargs['display_template'] = kwargs.pop('display_template')
        if 'display_func' in kwargs:
            widget_kwargs['display_func'] = kwargs.pop('display_func')
        self.widget = DynamicChoice(model, **widget_kwargs)

    def clean(self, value):
        """
        Validates that the input is a valid primary key for the model and
        that a model instance with the given primary key exists.
        """
        value = super(DynamicModelChoiceField, self).clean(value)
        if value in validators.EMPTY_VALUES:
            value = None
        else:
            try:
                value = self.model._meta.pk.to_python(value)
                value = self.model._default_manager.get(pk=value)
            except validators.ValidationError as e:
                raise forms.ValidationError(e.messages[0])
            except self.model.DoesNotExist:
                raise forms.ValidationError(
                    u'This field must specify an existing %s.' % \
                        capfirst(self.model._meta.verbose_name))
        return value

class DynamicChoice(forms.Widget):
    """
    Provides a hidden field to be manipulated on the client side when
    implementing dynamic selection of an instance of a given model, with
    the primary key of the selected instance being stored in the field.

    If a valid primary key has been specified, the string equivalent of
    the appropriate model instance will also be be displayed.
    """
    def __init__(self, model, attrs=None,
                 display_template=u' <span id="%(field_name)s_display">%(item)s</span>',
                 display_func=lambda x: unicode(x)):
        self.model = model
        self.attrs = attrs or {}
        self.display_template = display_template
        self.display_func = display_func

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type='hidden', name=name)
        item = ''
        if value != '':
            final_attrs['value'] = force_str(value)
            try:
                instance = self.model._default_manager.get(pk=value)
                item = escape(force_str(self.display_func(instance)))
            except self.model.DoesNotExist:
                pass
        display_text = self.display_template % {
            'field_name': name,
            'item': item,
        }
        return mark_safe(u'<input%s>%s' % (flatatt(final_attrs), display_text))

    def __deepcopy__(self, memo):
        """
        Implements deep copying to deep copy ``attrs`` and avoid any
        attempt to copy ``display_func``.
        """
        result = DynamicChoice(self.model, copy.deepcopy(self.attrs),
            self.display_template, self.display_func)
        memo[id(self)] = result
        return result

class MultipleDynamicModelChoiceField(forms.ChoiceField):
    def __init__(self, model, display_func=lambda x: unicode(x), *args, **kwargs):
        self.model = model
        self.display_func = display_func
        super(MultipleDynamicModelChoiceField, self).__init__(*args, **kwargs)
        self.widget = DynamicSelectMultiple(model, display_func=display_func)
        # HACK - assignment to self.initial in Field.__init__ isn't using
        #        the property this class defines.
        if 'initial' in kwargs:
            self.initial = kwargs['initial']

    def _get_initial(self):
        return self._initial

    def _set_initial(self, value):
        # Setting initial also sets choices on this field and the widget.
        # Accepts a list of instances or primary keys, which will be
        # looked up.
        self._initial = value
        if value is not None and len(value):
            if not isinstance(value[0], self.model):
                value = self.model._default_manager.filter(pk__in=value)
            self.choices = [(i.pk, self.display_func(i)) for i in value]

    initial = property(_get_initial, _set_initial)

    def clean(self, value):
        """
        Validates that the input is a list of valid primary keys for the
        model and that model instances with the given primary keys exist.
        """
        if self.required and not value:
            raise ValidationError(ugettext(u'This field is required.'))
        elif not self.required and not value:
            return []
        if not isinstance(value, (list, tuple)):
            raise ValidationError(ugettext(u'Enter a list of values.'))
        # Validate that each value in the value list is a valid primary key.
        pk_field = self.model._meta.pk
        final_values = []
        try:
            pk_values = [pk_field.to_python(v) for v in value]
            final_values = list(self.model._default_manager.filter(pk__in=pk_values))
            if len(pk_values) != len(final_values):
                raise forms.ValidationError(
                    u'This field must specify existing %s.' % \
                        capfirst(self.model._meta.verbose_name_plural))
        except validators.ValidationError as e:
            raise forms.ValidationError(e.messages[0])
        return final_values

class DynamicSelectMultiple(forms.Widget):
    """
    Provides a ``<select>`` element which is intended to be manipulated
    on the client side when implementing dynamic selection of a number of
    instances of a given model, rather than displaying a list of
    instances for selection.

    As such, ``<option>`` elements in the HTML ``<select>`` element this
    widget generates are always selected to ensure their resubmission,
    and if choices are not set when rendering, they are looked up using
    the primary key values which were previously submitted.
    """
    def __init__(self, model, attrs=None, choices=(),
                 display_func=lambda x: unicode(x)):
        self.model = model
        self.attrs = attrs or {}
        self.choices = choices
        self.display_func = display_func

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        if value and not self.choices:
            self.choices = [(i.pk, self.display_func(i)) for i in \
                            self.model._default_manager.filter(pk__in=value)]
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select multiple="multiple"%s>' % flatatt(final_attrs)]
        for option_value, option_label in chain(self.choices, choices):
            output.append(u'<option value="%s" selected="selected">%s</option>' % (
                escape(force_str(option_value)), escape(force_str(option_label))))
        output.append(u'</select>')
        return mark_safe(u'\n'.join(output))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name, None)

    def __deepcopy__(self, memo):
        """
        Implements deep copying to deep copy ``attrs`` and ``choices``,
        and to avoid any attempt to copy ``display_func``.
        """
        result = DynamicSelectMultiple(self.model, copy.deepcopy(self.attrs),
            copy.deepcopy(self.choices), self.display_func)
        memo[id(self)] = result
        return result