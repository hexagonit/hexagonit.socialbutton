from Products.CMFCore.utils import getToolByName
from five import grok
from hexagonit.socialbutton.browser.interfaces import IHexagonitSocialbuttonLayer
from plone.app.layout.viewlets.interfaces import IBelowContent
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
from zope.component import getMultiAdapter


grok.templatedir('viewlets')


class SocialButtonsViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.layer(IHexagonitSocialbuttonLayer)
    grok.name('hexagonit.socialbutton.viewlet')
    grok.require('zope2.View')
    grok.template('social-buttons')
    grok.viewletmanager(IViewletManager)


    def _normalize(self, value):
        """Normalize and make it list."""
        return [l.strip() for l in value.strip().splitlines() if l.strip()]

    @property
    def buttons(self):
        registry = getUtility(IRegistry)
        items = registry['hexagonit.socialbutton.config']
        keys = []
        types = getToolByName(self.context, 'portal_types')
        for key in items:
            if types.getTypeInfo(self.context).id not in items[key]['content_types']:
                continue
            if not items[key]['enabled']:
                continue
            if self.context.getLayout() not in self._normalize(items[key]['view_models']):
                continue
            if self.manager.__name__ not in self._normalize(items[key]['viewlet_manager']):
                continue
            keys.append(key)
        return keys

    def items(self):
        registry = getUtility(IRegistry)
        items = registry['hexagonit.socialbutton.codes']
        context_state = getMultiAdapter(
            (self.context, self.request), name='plone_context_state')
        portal_state = getMultiAdapter(
            (self.context, self.request), name='plone_portal_state')
        res = []
        for key in self.buttons:
            item = {'code_id': key}
            code_text = items[key]['code_text']
            lang = portal_state.language()
            code_text = code_text.format(
                URL=context_state.current_base_url(),
                LANG=lang,
                LANG_COUNTRY='{0}_{1}'.format(lang, items[key]['code_country']),
                ICON=items[key]['code_icon'])
            item['code_text'] = code_text
            res.append(item)
        return res
