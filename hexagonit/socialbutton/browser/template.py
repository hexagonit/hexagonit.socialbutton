from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from five import grok
from hexagonit.socialbutton import _
from hexagonit.socialbutton.data import Data
from hexagonit.socialbutton.interfaces import IData
from plone.app.z3cform.layout import wrap_form
from plone.registry.interfaces import IRegistry
from plone.z3cform.crud import crud
from zope.component import getUtility


grok.templatedir('templates')


class SocialButtonCodeForm(crud.CrudForm):
    """Form for updating social button code at ControlPanel."""

    label = _(u'Social Button Code Setting')
    update_schema = IData
    record_name = 'hexagonit.socialbutton.codes'

    def update(self):
        super(self.__class__, self).update()
        edit_forms = self.subforms[0]
        forms = edit_forms.subforms
        size = 50
        for form in forms:
            code_text_widget = form.widgets['code_text']
            code_text_widget.size = size
        add_form = self.subforms[1]
        add_form.widgets['code_text'].size = size

    def get_items(self):
        """Get items to show on the form."""
        registry = getUtility(IRegistry)
        items = registry[self.record_name]
        data = []
        if items is not None:
            for code_id, code_text in items.items():
                code_id = str(code_id)
                dat = Data(code_id, code_text)
                data.append(
                    (
                        code_id,
                        dat,
                    )
                )
        return data

    def add(self, data):
        """Add new data to hexagonit.socialbutton registry.

        :param data: data.
        :type data: dict
        """
        registry = getUtility(IRegistry)
        items = registry[self.record_name] or {}
        items.update(
            {unicode(data['code_id']): data['code_text']}
        )
        registry[self.record_name] = items

    def remove(self, (code_id, item)):
        """Delete data from hexagonit.socialbutton registry.

        :param code_id: Language code.
        :type code_id: str

        :param item: hexagonit.socialbutton.data.Data instance.
        :type item: obj
        """
        registry = getUtility(IRegistry)
        items = registry[self.record_name]
        del items[code_id]
        registry[self.record_name] = items


SocialButtonCodeControlPanelView = wrap_form(
    SocialButtonCodeForm,
    index=ViewPageTemplateFile('templates/controlpanel.pt')
)
