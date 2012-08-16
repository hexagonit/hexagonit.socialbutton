from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from five import grok
from hexagonit.socialbutton import _
from hexagonit.socialbutton.browser.interfaces import IHexagonitSocialbuttonLayer
from hexagonit.socialbutton.data import SocialButtonCode
from hexagonit.socialbutton.data import SocialButtonConfig
from hexagonit.socialbutton.interfaces import IAddSocialButtonCode
from hexagonit.socialbutton.interfaces import IAddSocialButtonConfig
from hexagonit.socialbutton.interfaces import ISocialButtonCode
from hexagonit.socialbutton.interfaces import ISocialButtonConfig
from plone.registry.interfaces import IRegistry
from plone.z3cform.crud import crud
from zope.component import getUtility


grok.templatedir('templates')


class BaseCrudForm(crud.CrudForm):
    """Base Crud Form"""

    def _convert_to_unicode(self, data):
        """Convert dictionary keys from sting to unicode and
        all types of values into unicode."""
        items = {}
        for key in data:
            value = data[key]
            key = unicode(key)
            if isinstance(value, bool):
                items[key] = unicode(value)
            elif isinstance(value, set):
                items[key] = u','.join(value)
            else:
                items[key] = value
        return items

    def add(self, data):
        """Add new data to registry.

        :param data: data.
        :type data: dict
        """
        data = self._convert_to_unicode(data)
        registry = getUtility(IRegistry)
        items = registry[self._record_name] or {}
        items[data.pop('code_id')] = data
        registry[self._record_name] = items

    def get_items(self):
        """Get items to show on the form."""
        registry = getUtility(IRegistry)
        items = registry[self._record_name]
        data = []
        if items is not None:
            for key in items:
                code_id = str(key)
                # if items[key].get(u'enabled'):
                #     instance = self._class(code_id, **self._convert_from_unicode(items[key]))
                # else:
                instance = self._class(code_id, **items[key])
                # instance = self._class(code_id, **self._convert_from_unicode(items[key]))
                data.append((code_id, instance))
        return data

    def remove(self, (code_id, item)):
        """Delete data from registry.

        :param code_id: ID for social button.
        :type code_id: unicode

        :param item: item instance.
        :type item: obj
        """
        registry = getUtility(IRegistry)
        items = registry[self._record_name]
        del items[code_id]
        registry[self._record_name] = items

    def before_update(self, item, data):
        """Update field values.

        :param item: data instance.
        :type item: object

        :param data: Field key and value.
        :type data: dict
        """
        registry = getUtility(IRegistry)
        items = registry[self._record_name]
        data = self._convert_to_unicode(data)
        items[item.code_id] = data
        registry[self._record_name] = items


class SocialButtonCodeForm(BaseCrudForm):
    """Form for updating social button code at ControlPanel."""
    label = _(u'Social Button Code Setting')
    update_schema = ISocialButtonCode
    _record_name = 'hexagonit.socialbutton.codes'
    _class = SocialButtonCode

    @property
    def add_schema(self):
        return IAddSocialButtonCode

    def update(self):
        super(self.__class__, self).update()
        edit_forms = self.subforms[0]
        forms = edit_forms.subforms
        cols = 70
        for form in forms:
            code_text_widget = form.widgets['code_text']
            code_text_widget.cols = cols
        add_form = self.subforms[1]
        add_form.widgets['code_text'].cols = cols


class SocialButtonConfigForm(BaseCrudForm):
    """Form for updating social button configuration at ControlPanel."""

    label = _(u'Social Button Configuration')
    update_schema = ISocialButtonConfig
    _record_name = 'hexagonit.socialbutton.config'
    _class = SocialButtonConfig

    @property
    def add_schema(self):
        return IAddSocialButtonConfig


class BaseControlPanelView(grok.View):
    grok.baseclass()
    grok.context(IPloneSiteRoot)
    grok.layer(IHexagonitSocialbuttonLayer)
    grok.template('controlpanel')

    def create_form(self, form_class):
        form = form_class(self.context, self.request)
        return form()


class SocialButtonCodeControlPanelView(BaseControlPanelView):
    grok.name('social-button-code-controlpanel')

    def form(self):
        return self.create_form(SocialButtonCodeForm)


class SocialButtonConfigControlPanelView(BaseControlPanelView):
    grok.name('social-button-config-controlpanel')

    def update(self):
        registry = getUtility(IRegistry)
        items = registry['hexagonit.socialbutton.codes']
        if not items:
            message = _(u"Please add code for social button first.")
            IStatusMessage(self.request).addStatusMessage(message, type='warn')
            return self.template

    def form(self):
        return self.create_form(SocialButtonConfigForm)
